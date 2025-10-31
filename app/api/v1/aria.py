from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.huggingface_service import HuggingFaceService

router = APIRouter()

class AriaRequest(BaseModel):
    message: str

class AriaResponse(BaseModel):
    response: str
    model: str = "Mistral-7B"
    provider: str = "HuggingFace"

@router.post("/chat", response_model=AriaResponse)
async def chat(request: AriaRequest):
    hf = HuggingFaceService()
    result = hf.chat(request.message)
    if result["success"]:
        return AriaResponse(response=result["response"])
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@router.get("/health")
async def health():
    return {"status": "ok", "provider": "HuggingFace"}
