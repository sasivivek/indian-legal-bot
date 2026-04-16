"""
India's Legal Voice — FastAPI Application
Main API server with endpoints for chat, TTS, translation, and health check.
Designed for Vercel serverless deployment via Mangum adapter.
"""

import os
import sys
import time
from pathlib import Path

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
    title="India's Legal Voice API",
    description="Multilingual AI-powered legal assistant for Indian laws",
    version="2.0.0",
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

class ChatResponse(BaseModel):
    response: str
    sources: list
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

_ai_service = None
_translation_service = None
_tts_service = None


def get_ai():
    global _ai_service
    if _ai_service is None:
        from api.ai_service import get_ai_service
        _ai_service = get_ai_service()
    return _ai_service


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
    Main chat endpoint. Accepts a legal question and returns an AI-generated response
    with relevant legal sources. Supports multilingual queries.
    """
    start_time = time.time()

    try:
        translator = get_translator()
        ai_service = get_ai()

        # Step 1: Translate query to English if needed
        query_english = request.query
        if request.language != "en":
            query_english = translator.translate_to_english(
                request.query, source_lang=request.language
            )

        # Step 2: Generate AI response (in English)
        result = await ai_service.generate_response(query_english, request.language)

        # Step 3: Translate response to target language if needed
        response_text = result["response"]
        if request.language != "en":
            response_text = translator.translate_from_english(
                response_text, target_lang=request.language
            )

        elapsed = time.time() - start_time
        print(f"Chat response generated in {elapsed:.2f}s (status={result['status']})")

        return ChatResponse(
            response=response_text,
            sources=result["sources"],
            language=request.language,
            status=result["status"],
            query_english=query_english,
        )

    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")


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
        print(f"TTS error: {e}")
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
        print(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint returning status of all services."""
    from api.translation_service import TRANSLATOR_AVAILABLE
    from api.tts_service import GTTS_AVAILABLE

    gemini_status = "available" if get_ai().model is not None else "unavailable (using fallback)"

    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "ai_gemini": gemini_status,
            "translation": "available" if TRANSLATOR_AVAILABLE else "unavailable",
            "tts": "available" if GTTS_AVAILABLE else "unavailable",
            "nlp_pipeline": "available",
        },
        "supported_languages": list(get_translator().get_supported_languages().keys()),
    }


@app.get("/api/languages")
async def get_languages():
    """Get list of supported languages with metadata."""
    return get_translator().get_supported_languages()


# ─── Static file serving (for local development) ─────────────────────────────

# Serve the frontend files for local dev
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
    print("\n>>> Starting India's Legal Voice API Server...")
    print("    Frontend: http://localhost:8000/")
    print("    API Docs: http://localhost:8000/docs")
    print("    Health:   http://localhost:8000/api/health\n")
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
