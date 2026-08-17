"""
Bharat Legal AI - Local Development Server
Starts the FastAPI backend with ChromaDB Vector RAG and the static frontend.
"""

import sys
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

load_dotenv()


def check_and_prepare_vector_index():
    """Verify if the ChromaDB vector index is built. If missing, build it automatically."""
    try:
        from api.vector_store import get_vector_store
        vector_store = get_vector_store()
        count = vector_store.count()

        if count == 0:
            print("[Startup] Vector database is empty or not yet indexed.")
            print("[Startup] Auto-building ChromaDB vector index from legal knowledge base...")
            from scripts.build_vector_index import build_index
            build_index()
        else:
            print(f"[Startup] Vector index verified: {count} document chunks ready in ChromaDB.")
    except Exception as e:
        print(f"[Startup] Note on vector store: {e}")
        print("[Startup] You can build the index manually using: python scripts/build_vector_index.py")


if __name__ == "__main__":
    print()
    print("  +==================================================+")
    print("  |         Bharat Legal AI Server (Vector RAG)      |")
    print("  |         Multilingual Indian Law Assistant        |")
    print("  +==================================================+")
    print("  |  Frontend:  http://localhost:8000/                |")
    print("  |  API Docs:  http://localhost:8000/docs            |")
    print("  |  Health:    http://localhost:8000/api/health      |")
    print("  +==================================================+")
    print()

    check_and_prepare_vector_index()

    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
