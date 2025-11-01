from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.v1.aria import router as aria_router

app = FastAPI(title="Verte IA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://verte-ia-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aria_router, prefix="/api/v1/aria", tags=["ARIA"])

@app.get("/")
async def root():
    return {"message": "Verte IA Backend online!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
