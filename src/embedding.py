import os
import psycopg2
from sqlalchemy import make_url
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext, Document
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.readers.file import PyMuPDFReader

class EmbeddingManager():
    def __init__(self, initial_filepath):
        self.vector_store = self._make_vector_store()
        self.index = self._make_index(initial_filepath)
        self.loaded_files = []

    def insert(self, filepath):
        if filepath not in self.loaded_files:
            self.loaded_files.append(filepath)
            docs = self.load_files(filepath)
            for doc in docs:
                self.index.insert(doc)
        return True

    def query_engine(self, llm):
        query_engine = self.index.as_query_engine(llm=llm, similarity_top_k = 5)
        return query_engine

    def load_files(self, path) -> list[Document]:
        if os.path.isdir(path):
            files = list(map(lambda x : path + "/" + x, os.listdir(path)))
        else:
            files = [path]
        
        documents = []
        for file in files:
            if file.split('.')[-1] == "pdf":
                loader = PyMuPDFReader()
                documents += loader.load(file_path=file)
            else:
                document = SimpleDirectoryReader(input_files=[file]).load_data()
                documents += document

        return documents

    def _make_index(self, filepath):

        files = self.load_files(filepath)

        if len(files) == 0:
            return None

        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        index = VectorStoreIndex.from_documents(
            documents = files, 
            storage_context=storage_context, show_progress=True,
            embed_model = Settings.embed_model
        )

        print(f"CREATED INDEX FOR {filepath}")
        return index

    def _make_vector_store(self):

        connection_string = "postgresql://postgres:postgres@localhost:5433"
        db_name = "vector_db"
        conn = psycopg2.connect(connection_string, password = "postgres")
        conn.autocommit = True

        print("CONNECTED TO DATABASE")

        with conn.cursor() as c:
            c.execute(f"DROP DATABASE IF EXISTS {db_name}")
            c.execute(f"CREATE DATABASE {db_name}")

        url = make_url(connection_string)
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name="ex_table",
            embed_dim=768,
            hnsw_kwargs={
                "hnsw_m": 32,
                "hnsw_ef_construction": 120,
                "hnsw_ef_search": 100,
                "hnsw_dist_method": "vector_cosine_ops",
            },
        )

        print("CREATED PGVECTOR_STORE")
        return vector_store