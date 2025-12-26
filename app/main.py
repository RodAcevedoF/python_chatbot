from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.chat_service import process_message

app = FastAPI(title="Hotel Costa Azul Chatbot")


@app.get("/")
def root():
    return {"status": "Chatbot activo"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply, intent, history = process_message(
        req.message,
        req.session_id or "default"
    )

    return ChatResponse(
        reply=reply,
        intent=intent,
        history=history
    )
