#!/usr/bin/env python
"""Run the MiPortafolio Backend API server"""

import sys
import uvicorn
from mportafolio_backend.config import API_HOST, API_PORT, API_RELOAD

if __name__ == "__main__":
    print(f"🚀 Starting MiPortafolio Backend API")
    print(f"   Host: {API_HOST}")
    print(f"   Port: {API_PORT}")
    print(f"   Reload: {API_RELOAD}")
    print(f"\n📖 API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"❤️  Health Check: http://{API_HOST}:{API_PORT}/health\n")

    uvicorn.run(
        "mportafolio_backend.api:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
        log_level="info"
    )
