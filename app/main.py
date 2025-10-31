from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import aria
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Verte IA - ARIA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aria.router, prefix="/api/v1/aria", tags=["ARIA"])

@app.get("/")
async def root():
    return {"message": "ARIA com Hugging Face!", "status": "online"}
