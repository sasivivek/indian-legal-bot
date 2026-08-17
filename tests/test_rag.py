"""
Bharat Legal AI — RAG Pipeline Automated Test Suite
Tests embeddings, ChromaDB vector store, retriever, thresholding, RAG generation, and FastAPI endpoints.
"""

import sys
import asyncio
from pathlib import Path
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.embeddings import get_embedding_service
from api.vector_store import get_vector_store
from api.retriever import get_retriever, LegalRetriever
from api.rag_pipeline import get_rag_pipeline, RAGPipeline
from api.index import chat, health_check, get_languages, ChatRequest
from scripts.build_vector_index import build_index


@pytest.fixture(scope="session", autouse=True)
def setup_vector_index():
    """Ensure the vector database index is built before running tests."""
    vector_store = get_vector_store()
    if vector_store.count() == 0:
        print("\n[Test Fixture] Building vector index for test suite...")
        build_index()
    return vector_store


class TestEmbeddings:
    """Test the SentenceTransformer embedding service."""

    def test_embedding_service_singleton(self):
        s1 = get_embedding_service()
        s2 = get_embedding_service()
        assert s1 is s2

    def test_single_query_embedding(self):
        service = get_embedding_service()
        vector = service.embed_query("What is Article 21?")
        assert isinstance(vector, list)
        assert len(vector) > 0
        assert isinstance(vector[0], float)

    def test_batch_texts_embedding(self):
        service = get_embedding_service()
        texts = [
            "Article 14 guarantees equality before law.",
            "Section 302 of Indian Penal Code deals with punishment for murder.",
            "RTI Act empowers citizens to seek information.",
        ]
        vectors = service.embed_texts(texts)
        assert len(vectors) == 3
        assert len(vectors[0]) == len(vectors[1]) == len(vectors[2])

    def test_empty_query_raises_error(self):
        service = get_embedding_service()
        with pytest.raises(ValueError):
            service.embed_query("")


class TestVectorStore:
    """Test ChromaDB persistent vector storage."""

    def test_vector_store_stats(self):
        store = get_vector_store()
        stats = store.get_collection_stats()
        assert stats["total_chunks"] > 0
        assert stats["is_indexed"] is True
        assert "bharat_legal_knowledge" in stats["collection_name"]

    def test_vector_similarity_search(self):
        store = get_vector_store()
        embedder = get_embedding_service()

        q_vec = embedder.embed_query("Right to life and personal liberty")
        results = store.search(q_vec, top_k=3)

        assert len(results["ids"][0]) == 3
        assert len(results["documents"][0]) == 3
        assert len(results["metadatas"][0]) == 3


class TestRetriever:
    """Test semantic retriever, acronym expansion, and distance thresholding."""

    def test_acronym_expansion(self):
        retriever = get_retriever()
        exp1 = retriever.preprocess_query("What is IPC 302?")
        assert "Indian Penal Code" in exp1

        exp2 = retriever.preprocess_query("How to file FIR under CrPC?")
        assert "First Information Report" in exp2
        assert "Code of Criminal Procedure" in exp2

        exp3 = retriever.preprocess_query("What is RTI?")
        assert "Right to Information" in exp3

    def test_retrieve_article_21(self):
        retriever = get_retriever()
        results = retriever.retrieve("What is Article 21 Right to Life?", top_k=3)
        assert len(results) > 0
        top_titles = [r.title for r in results]
        assert any("Article 21" in t for t in top_titles)
        assert results[0].similarity > 0.3

    def test_retrieve_article_14(self):
        retriever = get_retriever()
        results = retriever.retrieve("Right to equality before law", top_k=3)
        assert len(results) > 0
        top_titles = [r.title for r in results]
        assert any("Article 14" in t for t in top_titles)

    def test_retrieve_rti_act(self):
        retriever = get_retriever()
        results = retriever.retrieve("How to get information from government under RTI?", top_k=3)
        assert len(results) > 0
        top_titles = [r.title for r in results]
        assert any("Right to Information" in t or "RTI" in t for t in top_titles)

    def test_retrieve_consumer_rights(self):
        retriever = get_retriever()
        results = retriever.retrieve("How to file consumer complaint against defective product?", top_k=3)
        assert len(results) > 0
        top_cats = [r.category for r in results]
        assert "consumer" in top_cats

    def test_retrieve_cyber_crime(self):
        retriever = get_retriever()
        results = retriever.retrieve("What are the laws against online hacking and cyber crime in India?", top_k=3)
        assert len(results) > 0
        top_titles = [r.title for r in results]
        assert any("Information Technology" in t or "Cyber" in t for t in top_titles)

    def test_threshold_blocks_gibberish(self):
        retriever = get_retriever()
        # Set strict threshold for gibberish test
        results = retriever.retrieve("zxqkjw bzztrr qwopkjasdf987123 random nonsense text", threshold=0.4)
        assert len(results) == 0


class TestRAGPipeline:
    """Test full end-to-end RAG Q&A pipeline."""

    def test_rag_answer_article_21(self):
        rag = get_rag_pipeline()
        output = asyncio.run(rag.answer("What is Article 21 of the Indian Constitution?"))
        assert output.status in ("rag_generated", "rag_fallback")
        assert len(output.response) > 50
        assert len(output.sources) > 0
        assert any("Article 21" in s["title"] for s in output.sources)

    def test_rag_empty_query(self):
        rag = get_rag_pipeline()
        output = asyncio.run(rag.answer(""))
        assert output.status == "invalid_query"
        assert len(output.sources) == 0

    def test_rag_unrelated_query_no_context(self):
        # A query completely unrelated to Indian law with strict threshold
        retriever = LegalRetriever(threshold=0.3)
        rag = RAGPipeline(retriever=retriever)
        output = asyncio.run(rag.answer("How to bake chocolate chip cookies with sourdough?"))
        assert output.status == "no_relevant_context"
        assert "could not find sufficient information" in output.response.lower()


class TestFastAPIEndpoints:
    """Test FastAPI API endpoint handlers directly."""

    def test_health_check_endpoint(self):
        data = asyncio.run(health_check())
        assert data["status"] == "healthy"
        assert data["pipeline"] == "Vector_RAG_ChromaDB_Embeddings"
        assert data["services"]["vector_store_chromadb"]["total_chunks"] > 0
        assert len(data["supported_languages"]) == 10

    def test_languages_endpoint(self):
        langs = asyncio.run(get_languages())
        assert "en" in langs
        assert "hi" in langs
        assert "te" in langs
        assert "ta" in langs
        assert "kn" in langs
        assert "ml" in langs
        assert "bn" in langs
        assert "mr" in langs
        assert "pa" in langs
        assert "gu" in langs

    def test_chat_endpoint_english(self):
        req = ChatRequest(query="What are my rights under Article 19?", language="en")
        res = asyncio.run(chat(req))
        assert len(res.response) > 0
        assert len(res.sources) > 0
        assert res.language == "en"
        assert res.status in ("rag_generated", "rag_fallback")

    def test_chat_endpoint_hindi(self):
        req = ChatRequest(query="अनुच्छेद 21 क्या है?", language="hi")
        res = asyncio.run(chat(req))
        assert len(res.response) > 0
        assert res.language == "hi"
