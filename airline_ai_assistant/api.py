import base64
from io import BytesIO
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from utils.core import chat

app = FastAPI()

class ChatRequest(BaseModel):
    history: List[Dict[str, Any]]

class ChatResponse(BaseModel):
    history: List[Dict[str, Any]]
    audio_b64: Optional[str] = None
    image_b64: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    updated_history, voice_bytes, image_pil = chat(req.history)

    audio_b64 = base64.b64encode(voice_bytes).decode('utf-8') if voice_bytes else None

    image_b64 = None
    if image_pil:
        buffered = BytesIO()
        image_pil.save(buffered, format="PNG")
        image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return ChatResponse(
        history=updated_history,
        audio_b64=audio_b64,
        image_b64=image_b64
    )