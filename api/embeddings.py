"""
Bharat Legal AI — Embedding Service
Singleton wrapper around sentence-transformers for multilingual legal text embeddings.
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class EmbeddingService:
    """
    Singleton service for generating vector embeddings using SentenceTransformers.
    Supports 10+ Indian languages using multilingual models (default: paraphrase-multilingual-MiniLM-L12-v2).
    """

    _instance: Optional["EmbeddingService"] = None

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv(
            "EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2"
        )
        self._model = None
        self._embedding_dim = None

    @classmethod
    def get_instance(cls, model_name: Optional[str] = None) -> "EmbeddingService":
        """Get or initialize the singleton EmbeddingService instance."""
        if cls._instance is None:
            cls._instance = cls(model_name)
        return cls._instance

    @property
    def model(self):
        """Lazy load the sentence transformer model once."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                print(f"[Embeddings] Loading embedding model: {self.model_name}...")
                self._model = SentenceTransformer(self.model_name)
                # Compute dimension
                test_embed = self._model.encode(["test"])
                self._embedding_dim = len(test_embed[0])
                print(
                    f"[Embeddings] Model '{self.model_name}' loaded successfully (dim={self._embedding_dim})."
                )
            except Exception as e:
                print(f"[Embeddings] Error loading embedding model '{self.model_name}': {e}")
                raise RuntimeError(
                    f"Failed to load embedding model '{self.model_name}'. Ensure sentence-transformers is installed: {e}"
                )
        return self._model

    def embed_texts(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate normalized embeddings for a list of document chunk texts.
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return [emb.tolist() if hasattr(emb, "tolist") else list(emb) for emb in embeddings]

    def embed_query(self, query: str) -> List[float]:
        """
        Generate normalized embedding for a single user query string.
        """
        if not query or not query.strip():
            raise ValueError("Cannot generate embedding for empty query.")

        embedding = self.model.encode(
            [query.strip()],
            show_progress_bar=False,
            normalize_embeddings=True,
        )[0]
        return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)

    def get_model_info(self) -> Dict[str, Any]:
        """Return diagnostic info for health check."""
        return {
            "model_name": self.model_name,
            "is_loaded": self._model is not None,
            "dimension": self._embedding_dim or 384,
        }


# Helper factory function
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService.get_instance()
