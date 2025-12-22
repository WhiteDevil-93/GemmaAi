import os
import sys
from dotenv import load_dotenv

# LlamaIndex Imports
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    load_index_from_storage
)
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

load_dotenv()

class Devourer:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH_DEVOURER")
        if not self.model_path:
            raise ValueError("MODEL_PATH_DEVOURER not found in .env")
            
        print(f"LOADING DEVOURER (Background Worker): {self.model_path}")

        # 1. Setup LLM (27B Model) - CPU Focused
        # Low GPU layers effectively keeps it in RAM/CPU to avoid fighting Curator
        self.llm = LlamaCPP(
            model_path=self.model_path,
            temperature=0.1, 
            max_new_tokens=2048,
            context_window=32768, # Max context for deep reading
            model_kwargs={
                "n_gpu_layers": 0, # FORCE CPU for background stability
                "n_threads": int(os.getenv("THREADS", 8)),
            },
            verbose=True
        )

        # 2. Setup Embedding Model
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        # 3. Setup Vector Store (ChromaDB)
        self.chroma_client = chromadb.PersistentClient(path="./data/vectors")
        self.chroma_collection = self.chroma_client.get_or_create_collection("devourer_knowledge")
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        # 4. Load Index (No immediate ingestion to keep startup fast)
        self.index = self._load_index()

    def _load_index(self):
        if self.chroma_collection.count() > 0:
            return VectorStoreIndex.from_vector_store(
                self.vector_store, storage_context=self.storage_context
            )
        return None

    def ingest_data(self):
        """
        Scans data/input AND data/mobile.
        """
        dirs_to_scan = ["./data/input", "./data/mobile"]
        all_docs = []

        print(">> DEVOURER: Starting Multi-Source Ingestion...")

        for d in dirs_to_scan:
            if os.path.exists(d):
                print(f">> SCANNING: {d}")
                docs = SimpleDirectoryReader(d).load_data()
                all_docs.extend(docs)
        
        if not all_docs:
            return "No documents found in input or mobile folders."

        print(f">> DIGESTING: {len(all_docs)} documents...")
        if self.index is None:
             self.index = VectorStoreIndex.from_documents(
                all_docs, storage_context=self.storage_context
            )
        else:
            # Refresh/Update
            for doc in all_docs:
                self.index.insert(doc)
                
        return f"✔ Digested {len(all_docs)} documents from Local & Mobile sources."

    def query(self, message):
        if not self.index:
            return "No knowledge indexed yet."
        query_engine = self.index.as_query_engine()
        return str(query_engine.query(message))
