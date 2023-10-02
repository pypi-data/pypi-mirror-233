from annoy import AnnoyIndex
from src.db import Embedding, fullpath
import openai
import os
import pickle
import queue
import re
import sqlite3
import threading

class VectorDatabase:
    def __init__(self, db_file=".chatgpt-vectors.db"):
        db_path = fullpath(db_file)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode
        self.cursor = self.conn.cursor()
        self.create_schema()
        self.index = AnnoyIndex(1536, 'angular')
        self.embeddings = self.get_embeddings()
        for i, embedding in enumerate(self.embeddings):
            self.index.add_item(i, embedding.vector)
        self.index.build(10)

    def create_schema(self):
        query = """
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            message_id INTEGER,
            vector BLOB,
            phrase TEXT
        );
        """
        self.conn.execute(query)
        query = """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            last_message_id INTEGER
        );
        """
        self.conn.execute(query)

    def last_message_id(self):
        query = """
        SELECT last_message_id from progress
        """
        rows = self.conn.execute(query).fetchall()
        if not rows:
            return -1
        return rows[0][0]

    def commit_message(self, message_id):
        # Upsert into progress table
        query = """
        INSERT OR REPLACE INTO progress (id, last_message_id) VALUES (1, ?)
        """
        self.conn.execute(query, (message_id,))

        self.conn.commit()

    def add_embedding(self, vector, chat_id, message_id, phrase):
        query = """
        INSERT INTO embeddings (chat_id, message_id, vector, phrase) VALUES (?, ?, ?, ?)
        """
        # Serialize the vector to a binary format using pickle
        serialized_vector = pickle.dumps(vector)
        self.conn.execute(query, (chat_id, message_id, serialized_vector, phrase))
        self.conn.commit()

    def get_embeddings(self):  # Return List<Embedding>
        query = """
        SELECT * FROM embeddings
        """
        rows = self.conn.execute(query).fetchall()
        # Deserialize the vectors and return a list of Embedding objects
        return [Embedding(pickle.loads(row[3]), row[1], row[2]) for row in rows]

    def add(self, embedding: Embedding, phrase):  # Save to db
        self.add_embedding(
            embedding.vector, embedding.chat_id, embedding.message_id, phrase)
        self.embeddings.append(embedding)
        self.index.add_item(len(self.embeddings) - 1, embedding.vector)

    def find_neighbors(self, embedding: list, max_distance, max_results):
        # Annoy uses cosine similarity, so the distance is in the range [0, 2],
        # where 0 means identical and 2 means completely dissimilar
        ids, distances = self.index.get_nns_by_vector(
            embedding, max_results, include_distances=True)
        return [self.embeddings[i]
            for (i, distance) in zip(ids, distances)
            if distance <= max_distance]

def compute_embedding(text_string):
    model_id = "text-embedding-ada-002"
    return openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']

def chunk_string(text_string):
    if not text_string:
        return []
    try:
        sentence_endings = re.compile(r'[.!?\n]')
        sentence_list = sentence_endings.split(text_string)
        return [sentence.strip() for sentence in sentence_list if sentence]
    except Exception as e:
        print(f"{e} while chunking {text_string}")
        return []

class Future:
    def __init__(self):
        self._event = threading.Event()
        self._result = None

    def set_result(self, result):
        self._result = result
        self._event.set()

    def result(self):
        self._event.wait()
        return self._result

class SimilaritySearchEngine:
    def __init__(self):
        self.last_message_id_future = Future()
        self.db_file = ".chatgpt-vectors.db"
        self.exists = os.path.isfile(fullpath(self.db_file))
        self.add_queue = queue.Queue()
        self.search_queue = queue.Queue()
        self.combo = queue.Queue()
        self.worker_thread = threading.Thread(target=self.worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def worker(self):
        self.vector_db = VectorDatabase(self.db_file)
        self.last_message_id_future.set_result(self.vector_db.last_message_id())
        while True:
            result = self.combo.get()
            search = None
            add = None
            try:
                # First check the search queue
                search = self.search_queue.get_nowait()
            except queue.Empty:
                try:
                    # If the search queue is empty, check the add queue
                    add = self.add_queue.get_nowait()
                except queue.Empty:
                    continue

            if add:
                message_id = None
                for (embedding, phrase) in add:
                    message_id = embedding.message_id
                    self.vector_db.add(embedding, phrase)
                if message_id is not None:
                    self.vector_db.commit_message(message_id)

            if search:
                search_results = self.vector_db.find_neighbors(*search)
                result.put(search_results)

    def add(self, text_string, chat_id, message_id):
        chunks = chunk_string(text_string)
        items = [(self.embedding(chunk, chat_id, message_id), chunk) for chunk in chunks]
        print(f"Index of chat={chat_id} message={message_id}: {len(items)} phrases")
        self.add_queue.put(items)
        self.combo.put([])

    def embedding(self, chunk, chat_id, message_id):
        v = compute_embedding(chunk)
        return Embedding(v, chat_id,  message_id)

    # Returns a list of message IDs
    def search(self, text_string):
        embedding = compute_embedding(text_string)
        distance = 0.7
        for attempt in range(4):
            self.search_queue.put([embedding, distance, 10])
            result = queue.Queue()
            self.combo.put(result)
            elist = result.get()
            if elist:
                return [(e.chat_id, e.message_id) for e in elist]
            distance *= 1.2

    def last_message_id(self):
        return self.last_message_id_future.result()


