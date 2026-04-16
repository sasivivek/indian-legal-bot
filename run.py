"""
Bharat Legal AI - Local Development Server
Run this file to start the API server with the frontend.
"""

import uvicorn

if __name__ == "__main__":
    print()
    print("  +==================================================+")
    print("  |         Bharat Legal AI Server                    |")
    print("  |         Multilingual Indian Law Assistant         |")
    print("  +==================================================+")
    print("  |  Frontend:  http://localhost:8000/                |")
    print("  |  API Docs:  http://localhost:8000/docs            |")
    print("  |  Health:    http://localhost:8000/api/health      |")
    print("  +==================================================+")
    print()

    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
