from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.deepseek_service import deepseek_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_aria(request: ChatRequest):
    try:
        response_text = await deepseek_service.generate_response(request.message)
        return ChatResponse(status="success", response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
