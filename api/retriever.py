"""
Bharat Legal AI — Semantic Retriever Module
Embeds user queries, performs similarity search in ChromaDB, applies thresholding, and formats context.
"""

import os
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

from api.embeddings import get_embedding_service, EmbeddingService
from api.vector_store import get_vector_store, VectorStore

load_dotenv()


# Common Indian legal acronym expansions to boost semantic alignment
LEGAL_ACRONYMS = {
    r"\bipc\b": "Indian Penal Code",
    r"\bcrpc\b": "Code of Criminal Procedure",
    r"\bcpc\b": "Code of Civil Procedure",
    r"\bfir\b": "First Information Report",
    r"\brti\b": "Right to Information",
    r"\brte\b": "Right to Education",
    r"\bpil\b": "Public Interest Litigation",
    r"\bsc\b": "Supreme Court",
    r"\bhc\b": "High Court",
    r"\bdv act\b": "Domestic Violence Act",
    r"\bposh\b": "Prevention of Sexual Harassment",
    r"\bepf\b": "Employee Provident Fund",
    r"\besi\b": "Employee State Insurance",
    r"\bucc\b": "Uniform Civil Code",
    r"\bpocso\b": "Protection of Children from Sexual Offences",
    r"\bit act\b": "Information Technology Act",
    r"\bbns\b": "Bharatiya Nyaya Sanhita",
    r"\bbnss\b": "Bharatiya Nagarik Suraksha Sanhita",
    r"\bbsa\b": "Bharatiya Sakshya Adhiniyam",
}


@dataclass
class RetrievalResult:
    """Represents a single retrieved chunk with its distance score and legal metadata."""
    chunk_id: str
    text: str
    title: str
    category: str
    subcategory: str
    article: Optional[str] = None
    section: Optional[str] = None
    act: Optional[str] = None
    source: Optional[str] = None
    distance: float = 1.0  # Cosine distance (0.0 = identical, 1.0 = orthogonal)
    similarity: float = 0.0  # 1.0 - distance
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_source_dict(self) -> Dict[str, Any]:
        """Format for API response sources list."""
        return {
            "title": self.title,
            "category": self.category,
            "subcategory": self.subcategory,
            "article": self.article,
            "section": self.section,
            "act": self.act,
            "source": self.source,
            "similarity": round(self.similarity, 4),
        }


class LegalRetriever:
    """
    Retrieves relevant legal context chunks from ChromaDB using query embeddings and semantic similarity.
    """

    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        vector_store: Optional[VectorStore] = None,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ):
        self.embedding_service = embedding_service or get_embedding_service()
        self.vector_store = vector_store or get_vector_store()
        self.top_k = top_k or int(os.getenv("TOP_K", "5"))
        # Cosine distance threshold: distances <= threshold are considered relevant
        # Default 0.8 allows related legal topics while cutting out completely irrelevant text
        self.threshold = threshold if threshold is not None else float(
            os.getenv("RETRIEVAL_THRESHOLD", "0.8")
        )

    def preprocess_query(self, query: str) -> str:
        """
        Clean query and expand legal abbreviations for better semantic embedding match.
        """
        if not query:
            return ""

        processed = query.strip()

        # Expand acronyms case-insensitively
        for pattern, expansion in LEGAL_ACRONYMS.items():
            processed = re.sub(pattern, expansion, processed, flags=re.IGNORECASE)

        return processed

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> List[RetrievalResult]:
        """
        Execute full retrieval pipeline:
        1. Preprocess query (acronym expansion)
        2. Embed query vector
        3. Search ChromaDB vector store
        4. Apply distance threshold
        5. Map to RetrievalResult dataclasses
        """
        k = top_k or self.top_k
        thresh = threshold if threshold is not None else self.threshold

        clean_query = self.preprocess_query(query)
        if not clean_query:
            return []

        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(clean_query)

        # Query vector store
        search_output = self.vector_store.search(query_embedding=query_embedding, top_k=k)

        ids = search_output.get("ids", [[]])[0]
        documents = search_output.get("documents", [[]])[0]
        metadatas = search_output.get("metadatas", [[]])[0]
        distances = search_output.get("distances", [[]])[0]

        results: List[RetrievalResult] = []
        for chunk_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
            # In Chroma with cosine space: distance is (1 - cosine_similarity).
            # Lower distance means higher semantic similarity.
            if dist is not None and dist > thresh:
                # Exceeds distance threshold (too dissimilar)
                continue

            sim = max(0.0, 1.0 - float(dist)) if dist is not None else 0.0

            result = RetrievalResult(
                chunk_id=chunk_id,
                text=doc,
                title=meta.get("title", "Legal Document"),
                category=meta.get("category", "General"),
                subcategory=meta.get("subcategory", ""),
                article=meta.get("article") or None,
                section=meta.get("section") or None,
                act=meta.get("act") or None,
                source=meta.get("source") or meta.get("title", ""),
                distance=float(dist) if dist is not None else 1.0,
                similarity=sim,
                metadata=meta,
            )
            results.append(result)

        return results

    def format_context_for_prompt(self, results: List[RetrievalResult]) -> str:
        """
        Format retrieved chunks into a clean, structured context block for the RAG prompt.
        """
        if not results:
            return "No relevant legal provisions found in the knowledge base."

        context_blocks = []
        for i, res in enumerate(results, 1):
            header_parts = [f"[{i}] {res.title}"]
            if res.category:
                header_parts.append(f"Category: {res.category.title()}")
            if res.act:
                header_parts.append(f"Act: {res.act}")
            if res.article:
                header_parts.append(f"Article: {res.article}")
            if res.section:
                header_parts.append(f"Section: {res.section}")

            header = " | ".join(header_parts)
            block = f"{header}\n{res.text.strip()}"
            context_blocks.append(block)

        return "\n\n---\n\n".join(context_blocks)


# Helper factory function
def get_retriever() -> LegalRetriever:
    return LegalRetriever()
