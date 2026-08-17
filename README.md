# 🏛️ Bharat Legal AI — Multilingual Vector RAG Legal Assistant

A production-grade, multilingual legal AI assistant for **Indian Law and the Constitution of India**. Built with **Sentence-Transformers Embeddings**, **Persistent ChromaDB Vector Store**, **FastAPI**, **Google Gemini**, **Web Speech API (STT)**, and **gTTS (TTS)** across **10 Indian languages**.

---

## 📐 Architecture Overview

```text
                    USER INTERACTION
                           │
                 ┌─────────┴─────────┐
                 │                   │
             TEXT QUERY          VOICE INPUT
                 │                   │
                 │            Web Speech API
                 │             (10 Languages)
                 │                   │
                 └─────────┬─────────┘
                           ↓
                   FRONTEND UI (SPA)
             (Dark Glassmorphic Theme)
                           ↓
                  FASTAPI BACKEND
                 (POST /api/chat)
                           ↓
              MULTILINGUAL PROCESSING
            (Deep Translator → English)
                           ↓
                 QUERY PREPROCESSING
             (Legal Acronym Expansion)
                           ↓
                 QUERY EMBEDDING
        (paraphrase-multilingual-MiniLM-L12-v2)
                           ↓
               CHROMADB VECTOR STORE
             (Cosine Similarity Search)
                           ↓
                TOP-K RETRIEVAL RESULTS
             (Threshold Filtered Chunks)
                           ↓
              STRUCTURED RAG PROMPT
        (System Guardrails + Legal Context)
                           ↓
                 GOOGLE GEMINI AI
               (Grounded Generation)
                           ↓
                 GROUNDED LEGAL ANSWER
                           ↓
                 RESPONSE TRANSLATION
            (English → User's Language)
                           ↓
                 ┌─────────┴─────────┐
                 ↓                   ↓
             TEXT ANSWER         AUDIO SPEECH
          (+ Source Citations)   (gTTS Base64 MP3)
```

---

## 🧠 Core Technologies & Design Decisions

### 1. What are Embeddings & Why are They Used?
- **What**: Embeddings are dense numerical vectors (arrays of floating-point numbers) that capture the deep semantic meaning and relationships between words and sentences.
- **Why**: Traditional keyword search and TF-IDF only match exact word occurrences. An embedding model maps *"How can I get bail for my brother?"* and *"Section 437 CrPC non-bailable offences"* close to each other in vector space because they share legal meaning, even if they share zero vocabulary.
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions) — specifically optimized for multilingual semantic similarity across 50+ languages including English, Hindi, Bengali, Telugu, Tamil, and Marathi.

### 2. What is ChromaDB & Why is It Used?
- **What**: ChromaDB is an open-source, AI-native persistent vector database designed for lightning-fast similarity search over dense embeddings using Hierarchical Navigable Small World (HNSW) graphs.
- **Why**: It persists document embeddings locally on disk, supports rich metadata filtering (Title, Category, Article, Section, Act), and uses Cosine Distance metrics without needing external cloud database infrastructure.

### 3. What is RAG (Retrieval-Augmented Generation)?
- **What**: RAG is an architectural pattern that retrieves relevant factual context from a private knowledge base and injects it into the prompt before sending it to an LLM.
- **Why**: Standard LLMs can hallucinate legal section numbers, invent outdated amendments, or misquote articles. RAG guarantees that Gemini answers **only** using verified statutory texts from the database.

---

## 🌐 Supported Indian Languages (10 Languages)

| Code | Language | Native Script | Speech Code (STT/TTS) |
|:---:|:---|:---|:---|
| `en` | English | English | `en-IN` |
| `hi` | Hindi | हिन्दी | `hi-IN` |
| `te` | Telugu | తెలుగు | `te-IN` |
| `ta` | Tamil | தமிழ் | `ta-IN` |
| `kn` | Kannada | ಕನ್ನಡ | `kn-IN` |
| `ml` | Malayalam | മലയാളം | `ml-IN` |
| `bn` | Bengali | বাংলা | `bn-IN` |
| `mr` | Marathi | मराठी | `mr-IN` |
| `pa` | Punjabi | ਪੰਜਾਬੀ | `pa-IN` |
| `gu` | Gujarati | ગુજરાતી | `gu-IN` |

---

## 📁 Project Structure

```text
indian-legal-bot/
│
├── api/                               # Backend Application Package
│   ├── __init__.py
│   ├── index.py                       # FastAPI application & API endpoints
│   ├── legal_knowledge.py             # 40+ statutory Indian legal entries
│   ├── embeddings.py                  # Singleton Sentence-Transformers service
│   ├── vector_store.py                # ChromaDB persistent vector database wrapper
│   ├── retriever.py                   # Semantic retriever with thresholding & acronyms
│   ├── rag_pipeline.py                # RAG orchestration, prompt guardrails & fallback
│   ├── ai_service.py                  # Google Gemini API wrapper
│   ├── translation_service.py         # 10-language deep-translator service
│   └── tts_service.py                 # gTTS Text-to-Speech audio generation
│
├── scripts/
│   └── build_vector_index.py          # Offline document chunking & ChromaDB indexer
│
├── data/
│   └── chroma/                        # Persistent ChromaDB vector database files
│
├── public/                            # Web Frontend (SPA)
│   ├── index.html                     # Chat interface, voice controls, sidebar
│   ├── style.css                      # Glassmorphic dark design system
│   └── app.js                         # Web Speech API STT, Audio TTS, language switcher
│
├── tests/
│   └── test_rag.py                    # 20 automated pytest tests for RAG pipeline
│
├── run.py                             # Local development server with auto-index check
├── requirements.txt                   # Python dependencies
├── vercel.json                        # Deployment configuration
├── .env.example                       # Environment variables template
└── README.md                          # Documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+ (Python 3.10 - 3.12 recommended)
- Google Gemini API Key (get free at [aistudio.google.com](https://aistudio.google.com/))

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/sasivivek/indian-legal-bot.git
cd indian-legal-bot

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` from `.env.example`:

```bash
copy .env.example .env
```

Edit `.env` and set your `GEMINI_API_KEY`:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
CHROMA_PERSIST_DIRECTORY=./data/chroma
CHROMA_COLLECTION_NAME=bharat_legal_knowledge
TOP_K=5
RETRIEVAL_THRESHOLD=0.8
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

### 3. Build the Vector Index

Run the ingestion script to chunk the legal knowledge base, generate embeddings, and build the ChromaDB database:

```bash
python scripts/build_vector_index.py
```

*Output:*
```text
=================================================================
      BHARAT LEGAL AI — VECTOR INDEX INGESTION PIPELINE
=================================================================
[1/5] Loading legal knowledge base...
      Loaded 40 legal entries.
[2/5] Creating documents and semantic chunks (size=500, overlap=100)...
      Total Documents: 40
      Total Chunks:    168
[3/5] Loading Multilingual Embedding Model...
      Model: paraphrase-multilingual-MiniLM-L12-v2
[4/5] Generating Vector Embeddings for 168 chunks...
      Generated 168 embeddings (dimension=384).
[5/5] Indexing into Persistent ChromaDB Vector Store...
=================================================================
      INDEXING SUMMARY
=================================================================
  • Collection Name:     bharat_legal_knowledge
  • Storage Path:        .../data/chroma
  • Indexed Vectors:     168
  • Embedding Model:     paraphrase-multilingual-MiniLM-L12-v2 (384D)
  • Status:              READY FOR RAG RETRIEVAL
=================================================================
```

### 4. Run the Application

```bash
python run.py
```

Open your browser and navigate to:
- **Frontend App**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 🧪 Automated Testing

Run the full pytest suite (20 tests covering embeddings, vector store, retriever, thresholding, RAG generation, and API endpoints):

```bash
python -m pytest tests/test_rag.py -v
```

*All 20 tests pass:*
```text
tests/test_rag.py::TestEmbeddings::test_embedding_service_singleton PASSED
tests/test_rag.py::TestEmbeddings::test_single_query_embedding PASSED
tests/test_rag.py::TestEmbeddings::test_batch_texts_embedding PASSED
tests/test_rag.py::TestEmbeddings::test_empty_query_raises_error PASSED
tests/test_rag.py::TestVectorStore::test_vector_store_stats PASSED
tests/test_rag.py::TestVectorStore::test_vector_similarity_search PASSED
tests/test_rag.py::TestRetriever::test_acronym_expansion PASSED
tests/test_rag.py::TestRetriever::test_retrieve_article_21 PASSED
tests/test_rag.py::TestRetriever::test_retrieve_article_14 PASSED
tests/test_rag.py::TestRetriever::test_retrieve_rti_act PASSED
tests/test_rag.py::TestRetriever::test_retrieve_consumer_rights PASSED
tests/test_rag.py::TestRetriever::test_retrieve_cyber_crime PASSED
tests/test_rag.py::TestRetriever::test_threshold_blocks_gibberish PASSED
tests/test_rag.py::TestRAGPipeline::test_rag_answer_article_21 PASSED
tests/test_rag.py::TestRAGPipeline::test_rag_empty_query PASSED
tests/test_rag.py::TestRAGPipeline::test_rag_unrelated_query_no_context PASSED
tests/test_rag.py::TestFastAPIEndpoints::test_health_check_endpoint PASSED
tests/test_rag.py::TestFastAPIEndpoints::test_languages_endpoint PASSED
tests/test_rag.py::TestFastAPIEndpoints::test_chat_endpoint_english PASSED
tests/test_rag.py::TestFastAPIEndpoints::test_chat_endpoint_hindi PASSED
======================= 20 passed in 24.81s ========================
```

---

## 🔌 API Reference

### 1. `POST /api/chat`
Submit a legal query in any supported language and receive a grounded RAG response with source citations.

**Request:**
```json
{
  "query": "What is Article 21 of the Indian Constitution?",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "## 📋 Legal Summary: Article 21 — Right to Life and Personal Liberty\n\nArticle 21 of the Constitution of India guarantees that no person shall be deprived of his life or personal liberty except according to procedure established by law...",
  "sources": [
    {
      "title": "Article 21 — Right to Life and Personal Liberty",
      "category": "constitution",
      "subcategory": "fundamental_rights",
      "article": "21",
      "section": null,
      "act": "Constitution of India",
      "source": "Constitution of India",
      "similarity": 0.8412
    }
  ],
  "language": "en",
  "status": "rag_generated",
  "query_english": "What is Article 21 of the Indian Constitution?"
}
```

### 2. `POST /api/tts`
Converts text into audio speech using gTTS. Returns base64 MP3.

**Request:**
```json
{
  "text": "अनुच्छेद 21 जीवन और व्यक्तिगत स्वतंत्रता के अधिकार की रक्षा करता है।",
  "language": "hi"
}
```

**Response:**
```json
{
  "audio_base64": "//uQxAAAAAAAAAAAAAAAAAAAAAA...",
  "mime_type": "audio/mp3",
  "status": "success"
}
```

### 3. `GET /api/health`
Returns live status of embedding model, ChromaDB index, Gemini configuration, and language pipelines.

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "pipeline": "Vector_RAG_ChromaDB_Embeddings",
  "services": {
    "gemini_ai": {
      "configured": true,
      "model": "gemini-2.0-flash",
      "initialized": true
    },
    "embedding_model": {
      "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
      "is_loaded": true,
      "dimension": 384
    },
    "vector_store_chromadb": {
      "collection_name": "bharat_legal_knowledge",
      "persist_directory": "c:\\Users\\DELL\\Downloads\\indian-legal-bot-main\\data\\chroma",
      "total_chunks": 168,
      "is_indexed": true
    },
    "translation": "available",
    "tts": "available"
  },
  "supported_languages": ["en", "hi", "te", "ta", "kn", "ml", "bn", "mr", "gu", "pa"]
}
```

---

## ⚖️ Legal Disclaimer & Notice

This AI assistant provides **general legal information only** based on statutory records for educational purposes. It does not constitute formal legal advice and does not establish an attorney-client relationship. Please consult a licensed advocate or contact [NALSA](https://nalsa.gov.in) (Toll-Free 15100) for representation.

*Note on Legal Reforms*: India enacted the Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA) replacing the IPC, CrPC, and Evidence Act. The knowledge base contains foundational references which can be continuously updated with newer statutory enactments.

---

## 📄 License

MIT License © 2026 Bharat Legal AI.
