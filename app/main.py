from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import aria
import os

app = FastAPI(title="Verte IA Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://verte-ia-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(aria.router, prefix="/api/v1/aria", tags=["ARIA"])

@app.get("/")
async def root():
    return {"message": "Verte IA Backend online!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
