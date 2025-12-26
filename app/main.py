from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.schemas import ChatRequest, ChatResponse
from app.chat_service import process_message
from app.data_loader import load_hotel_info
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import subprocess
import sys
import os
from pathlib import Path

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Hotel Costa Azul Chatbot")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Get allowed origins from environment or use default for development
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:*,http://127.0.0.1:*").split(",")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS[0] != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Mount static files for UI
UI_DIR = Path(__file__).parent / "ui"
app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")


@app.get("/robots.txt")
def robots_txt():
    """Serve robots.txt from root to prevent search engine indexing."""
    from fastapi.responses import FileResponse
    return FileResponse(UI_DIR / "robots.txt", media_type="text/plain")


@app.get("/")
@limiter.limit("30/minute")
def root(request: Request):
    """Redirect root to UI."""
    return RedirectResponse(url="/ui/index.html")


@app.get("/health")
def health_check():
    """Health check endpoint for Render and monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/hotel-info")
@limiter.limit("60/minute")
def get_hotel_info(request: Request):
    """Get complete hotel information."""
    return load_hotel_info()


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")  # Prevent abuse - 20 messages per minute per IP
def chat(request: Request, req: ChatRequest):
    # Input validation
    if not req.message or len(req.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(req.message) > 1000:
        raise HTTPException(status_code=400, detail="Message too long (max 1000 characters)")
    
    # Sanitize session_id
    session_id = req.session_id or "default"
    if len(session_id) > 100:
        raise HTTPException(status_code=400, detail="Session ID too long")
    
    try:
        reply, intent, history = process_message(
            req.message.strip(),
            session_id
        )

        return ChatResponse(
            reply=reply,
            intent=intent,
            history=history
        )
    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing message")


@app.post("/reindex")
@limiter.limit("3/hour")  # Very strict rate limit for admin endpoint
def reindex_hotel_data(
    request: Request,
    x_api_key: str = Header(None)
):
    """Trigger re-indexing of hotel data into Supabase vector store.
    
    Requires ADMIN_API_KEY in header for security.
    """
    # Require API key for admin operations
    if ADMIN_API_KEY and x_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )
    
    try:
        # Run the embeddings script
        result = subprocess.run(
            [sys.executable, "-m", "app.scripts.embeddings_test"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Hotel data re-indexed successfully",
                "output": result.stdout
            }
        else:
            return {
                "status": "error",
                "message": "Re-indexing failed",
                "error": result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Re-indexing timed out"
        }
    except Exception as e:
        print(f"Re-indexing error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
