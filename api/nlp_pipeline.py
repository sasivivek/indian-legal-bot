"""
NLP Retrieval Pipeline
TF-IDF vectorization + cosine similarity search for relevant legal content.
Performs semantic matching of user queries against the legal knowledge base.
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from api.legal_knowledge import get_all_legal_entries, get_entry_text


class LegalNLPPipeline:
    """Retrieval-based NLP pipeline for Indian legal knowledge."""

    def __init__(self):
        self.entries = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._build_index()

    def _build_index(self):
        """Build TF-IDF index from the legal knowledge base."""
        self.entries = get_all_legal_entries()
        if not self.entries:
            return

        # Prepare corpus
        corpus = [get_entry_text(entry) for entry in self.entries]

        # Train TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Search legal knowledge base for relevant entries.

        Args:
            query: User's legal question
            top_k: Number of top results to return

        Returns:
            List of dicts with 'entry' and 'score' keys, sorted by relevance.
        """
        if not self.entries or self.vectorizer is None:
            return []

        # Preprocess query
        processed_query = self._preprocess_query(query)

        # TF-IDF similarity search
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Apply keyword boosting
        boosted_scores = self._apply_keyword_boost(query, similarities)

        # Get top-K results
        top_indices = np.argsort(boosted_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(boosted_scores[idx])
            if score > 0.01:  # Minimum threshold
                results.append({
                    "entry": self.entries[idx],
                    "score": round(score, 4),
                })

        return results

    def _preprocess_query(self, query: str) -> str:
        """Clean and normalize the query for search."""
        query = query.lower().strip()

        # Expand common legal abbreviations
        abbreviations = {
            r"\bipc\b": "indian penal code",
            r"\bcrpc\b": "code of criminal procedure",
            r"\bcpc\b": "code of civil procedure",
            r"\bfir\b": "first information report",
            r"\brti\b": "right to information",
            r"\brte\b": "right to education",
            r"\bpil\b": "public interest litigation",
            r"\bsc\b": "supreme court",
            r"\bhc\b": "high court",
            r"\bdv act\b": "domestic violence act",
            r"\bposh\b": "prevention of sexual harassment",
            r"\bepf\b": "employee provident fund",
            r"\besi\b": "employee state insurance",
            r"\bucc\b": "uniform civil code",
            r"\bpocso\b": "protection of children from sexual offences",
        }

        for abbr, expansion in abbreviations.items():
            query = re.sub(abbr, f"{expansion}", query)

        return query

    def _apply_keyword_boost(self, query: str, similarities: np.ndarray) -> np.ndarray:
        """
        Boost scores for entries that match specific legal identifiers
        like article numbers, section numbers, or exact legal terms.
        """
        boosted = similarities.copy()
        query_lower = query.lower()

        for idx, entry in enumerate(self.entries):
            boost = 0.0

            # Exact ID match (e.g., "article 21", "section 302")
            entry_id = entry.get("id", "").lower()
            id_parts = entry_id.replace("-", " ")
            if id_parts and id_parts in query_lower:
                boost += 0.5

            # Check for article/section number patterns
            numbers = re.findall(r"\b(\d+[a-z]?)\b", query_lower)
            for num in numbers:
                if num in entry_id:
                    boost += 0.3

            # Exact keyword match
            keywords = entry.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    boost += 0.15

            # Category mention boost
            category = entry.get("category", "")
            subcategory = entry.get("subcategory", "")
            if category and category in query_lower:
                boost += 0.1
            if subcategory and subcategory.replace("_", " ") in query_lower:
                boost += 0.1

            boosted[idx] += boost

        return boosted

    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        """
        Get formatted legal context string for AI response generation.

        Args:
            query: User's legal question
            top_k: Number of top results to include in context

        Returns:
            Formatted context string with relevant legal information.
        """
        results = self.search(query, top_k=top_k)

        if not results:
            return "No specific legal information found in the knowledge base for this query."

        context_parts = []
        for i, result in enumerate(results, 1):
            entry = result["entry"]
            score = result["score"]

            part = f"--- Source {i} (relevance: {score}) ---\n"
            part += f"Title: {entry.get('title', 'Unknown')}\n"
            part += f"Category: {entry.get('category', 'General')}\n"
            part += f"Content: {entry.get('content', '')}\n"
            part += f"Explanation: {entry.get('explanation', '')}\n"

            if "guidance" in entry:
                part += "Guidance:\n"
                for g in entry["guidance"]:
                    part += f"  • {g}\n"

            if "steps" in entry:
                part += "Steps:\n"
                for j, step in enumerate(entry["steps"], 1):
                    part += f"  {j}. {step}\n"

            context_parts.append(part)

        return "\n".join(context_parts)


# Singleton instance
_pipeline_instance = None


def get_pipeline() -> LegalNLPPipeline:
    """Get or create the singleton NLP pipeline instance."""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = LegalNLPPipeline()
    return _pipeline_instance
