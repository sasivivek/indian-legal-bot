"""
Bharat Legal AI — FastAPI Application
Main API server with endpoints for RAG chat, TTS, translation, and health check.
Powered by Sentence-Transformers, ChromaDB Vector Store, and Google Gemini.
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Bharat Legal AI API",
    description="Multilingual AI-powered Indian legal assistant using Vector RAG and Gemini",
    version="3.0.0",
)

# CORS middleware — allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User's legal question")
    language: str = Field(default="en", description="Language code (en, hi, te, ta, kn, ml, bn, mr, gu, pa)")

class SourceItem(BaseModel):
    title: str = ""
    category: str = ""
    subcategory: str = ""
    article: Optional[str] = None
    section: Optional[str] = None
    act: Optional[str] = None
    source: Optional[str] = None
    similarity: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    language: str
    status: str
    query_english: str = ""

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    language: str = Field(default="en", description="Language code for TTS")

class TTSResponse(BaseModel):
    audio_base64: str
    mime_type: str
    status: str

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    source_lang: str = Field(default="auto", description="Source language code")
    target_lang: str = Field(default="en", description="Target language code")

class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    status: str


# ─── Lazy-loaded services (avoid import cost on cold start) ───────────────────

_rag_pipeline = None
_translation_service = None
_tts_service = None


def get_rag():
    global _rag_pipeline
    if _rag_pipeline is None:
        from api.rag_pipeline import get_rag_pipeline
        _rag_pipeline = get_rag_pipeline()
    return _rag_pipeline


def get_translator():
    global _translation_service
    if _translation_service is None:
        from api.translation_service import get_translation_service
        _translation_service = get_translation_service()
    return _translation_service


def get_tts():
    global _tts_service
    if _tts_service is None:
        from api.tts_service import get_tts_service
        _tts_service = get_tts_service()
    return _tts_service


# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main RAG chat endpoint:
    1. Translates non-English query to English
    2. Performs semantic similarity search against ChromaDB vector store
    3. Assembles prompt with retrieved legal context
    4. Generates grounded answer via Gemini AI (or structured fallback)
    5. Translates response to requested language
    """
    start_time = time.time()

    try:
        translator = get_translator()
        rag_pipeline = get_rag()

        # Step 1: Translate query to English if needed for semantic retrieval
        query_english = request.query.strip()
        if request.language != "en":
            try:
                query_english = translator.translate_to_english(
                    request.query, source_lang=request.language
                )
            except Exception as te:
                print(f"[API] Translation to English failed ({te}), using original query...")
                query_english = request.query.strip()

        # Step 2: Execute Vector RAG Pipeline (Retrieve from ChromaDB + Generate with Gemini)
        rag_output = await rag_pipeline.answer(query=query_english)

        # Step 3: Translate response back to user's target language if needed
        final_response_text = rag_output.response
        if request.language != "en" and rag_output.status != "invalid_query":
            try:
                final_response_text = translator.translate_from_english(
                    final_response_text, target_lang=request.language
                )
            except Exception as te:
                print(f"[API] Translation from English failed ({te}), returning English text.")

        elapsed = time.time() - start_time
        print(f"[API] Chat RAG completed in {elapsed:.2f}s (status={rag_output.status}, chunks={len(rag_output.sources)})")

        return ChatResponse(
            response=final_response_text,
            sources=rag_output.sources,
            language=request.language,
            status=rag_output.status,
            query_english=query_english,
        )

    except Exception as e:
        print(f"[API] Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your legal query. Please try again."
        )


@app.post("/api/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """
    Text-to-Speech endpoint. Converts text to audio in the specified language.
    Returns base64-encoded MP3 audio.
    """
    try:
        tts_service = get_tts()
        result = tts_service.generate_audio(request.text, request.language)

        return TTSResponse(
            audio_base64=result["audio_base64"],
            mime_type=result["mime_type"],
            status=result["status"],
        )

    except Exception as e:
        print(f"[API] TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translation endpoint. Translates text between supported Indian languages.
    """
    try:
        translator = get_translator()
        result = translator.translate(
            request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )

        return TranslateResponse(
            translated_text=result["translated_text"],
            source_lang=result["source_lang"],
            target_lang=result["target_lang"],
            status=result["status"],
        )

    except Exception as e:
        print(f"[API] Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint returning diagnostic status of:
    - FastAPI
    - Gemini AI Configuration
    - Sentence-Transformers Embedding Model
    - ChromaDB Vector Store & Indexed Chunks Count
    - Translation Service
    - TTS Service
    """
    from api.translation_service import TRANSLATOR_AVAILABLE
    from api.tts_service import GTTS_AVAILABLE
    from api.embeddings import get_embedding_service
    from api.vector_store import get_vector_store
    from api.ai_service import get_ai_service

    embedding_info = get_embedding_service().get_model_info()
    vector_stats = get_vector_store().get_collection_stats()
    ai_status = get_ai_service().get_status()

    return {
        "status": "healthy",
        "version": "3.0.0",
        "pipeline": "Vector_RAG_ChromaDB_Embeddings",
        "services": {
            "gemini_ai": ai_status,
            "embedding_model": embedding_info,
            "vector_store_chromadb": vector_stats,
            "translation": "available" if TRANSLATOR_AVAILABLE else "unavailable",
            "tts": "available" if GTTS_AVAILABLE else "unavailable",
        },
        "supported_languages": list(get_translator().get_supported_languages().keys()),
    }


@app.get("/api/languages")
async def get_languages():
    """Get list of supported languages with metadata."""
    return get_translator().get_supported_languages()


# ─── Static file serving (for local development) ─────────────────────────────

frontend_dir = Path(__file__).parent.parent / "public"
if frontend_dir.exists():
    @app.get("/")
    async def serve_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        raise HTTPException(status_code=404, detail="Frontend not found")

    @app.get("/style.css")
    async def serve_css():
        return FileResponse(str(frontend_dir / "style.css"), media_type="text/css")

    @app.get("/app.js")
    async def serve_js():
        return FileResponse(str(frontend_dir / "app.js"), media_type="application/javascript")

    # Catch-all for other static assets
    app.mount("/", StaticFiles(directory=str(frontend_dir)), name="static")


# ─── Vercel Serverless Adapter ────────────────────────────────────────────────

try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = None


# ─── Local Development Server ────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("\n>>> Starting Bharat Legal AI (Vector RAG) Server...")
    print("    Frontend: http://localhost:8000/")
    print("    API Docs: http://localhost:8000/docs")
    print("    Health:   http://localhost:8000/api/health\n")
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
