"""
Bharat Legal AI — Vector Database Service
Persistent local ChromaDB wrapper for storing and querying legal vector embeddings with rich metadata.
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class VectorStore:
    """
    Persistent ChromaDB vector database wrapper.
    Stores document chunks, their embeddings, and associated legal metadata (article, section, category, act, source).
    """

    _instance: Optional["VectorStore"] = None

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIRECTORY", "./data/chroma"
        )
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION_NAME", "bharat_legal_knowledge"
        )
        self._client = None
        self._collection = None

    @classmethod
    def get_instance(
        cls,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
    ) -> "VectorStore":
        """Get or initialize the singleton VectorStore instance."""
        if cls._instance is None:
            cls._instance = cls(persist_directory, collection_name)
        return cls._instance

    @property
    def client(self):
        """Lazy load the persistent ChromaDB client."""
        if self._client is None:
            import chromadb
            from chromadb.config import Settings

            # Resolve absolute path for persistence
            db_path = Path(self.persist_directory).resolve()
            db_path.mkdir(parents=True, exist_ok=True)

            print(f"[VectorStore] Initializing ChromaDB persistent client at: {db_path}")
            self._client = chromadb.PersistentClient(
                path=str(db_path),
                settings=Settings(anonymized_telemetry=False),
            )
        return self._client

    @property
    def collection(self):
        """Get or create the target ChromaDB collection configured for cosine distance."""
        if self._collection is None:
            # Cosine distance: 0.0 is identical, 1.0 is orthogonal, 2.0 is opposite
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def add_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """
        Add or upsert documents, embeddings, and metadata into ChromaDB.
        """
        if not ids or not texts or not embeddings:
            return

        # Ensure all metadata values are primitive types accepted by Chroma (str, int, float, bool)
        clean_metadatas = []
        for meta in metadatas:
            clean_meta = {}
            for k, v in meta.items():
                if v is None:
                    clean_meta[k] = ""
                elif isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                elif isinstance(v, list):
                    clean_meta[k] = ", ".join(str(item) for item in v)
                else:
                    clean_meta[k] = str(v)
            clean_metadatas.append(clean_meta)

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=clean_metadatas,
        )
        print(f"[VectorStore] Upserted {len(ids)} document chunks into '{self.collection_name}'.")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute similarity search against ChromaDB using query vector embedding.
        Returns Chroma query results containing ids, documents, metadatas, and distances.
        """
        if self.count() == 0:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        actual_k = min(top_k, self.count())
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return results

    def count(self) -> int:
        """Return the number of vectors stored in the collection."""
        try:
            return self.collection.count()
        except Exception:
            return 0

    def clear_collection(self) -> None:
        """Delete and recreate the collection (used for rebuilding index)."""
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"[VectorStore] Deleted collection '{self.collection_name}'.")
        except Exception:
            pass
        self._collection = None
        # Recreate fresh collection
        _ = self.collection

    def get_collection_stats(self) -> Dict[str, Any]:
        """Return diagnostic info for health checks."""
        try:
            total_count = self.count()
            return {
                "collection_name": self.collection_name,
                "persist_directory": str(Path(self.persist_directory).resolve()),
                "total_chunks": total_count,
                "is_indexed": total_count > 0,
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "error": str(e),
                "is_indexed": False,
            }


# Helper factory function
def get_vector_store() -> VectorStore:
    return VectorStore.get_instance()
