from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from services.deepseek_service import aria_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"  # Para memória de conversa

class ChatResponse(BaseModel):
    status: str
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_aria(request: ChatRequest):
    try:
        response_text = await aria_service.generate_response(
            request.message, 
            request.user_id
        )
        return ChatResponse(status="success", response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
