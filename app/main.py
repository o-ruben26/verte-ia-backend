from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="Verte IA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

# Respostas inteligentes da ARIA
RESPOSTAS_ARIA = {
    "olá": "Olá! Eu sou a ARIA 😊 Sua assistente da Verte IA! Como posso ajudar?",
    "oi": "Oi! Que bom te ver! Sou a ARIA, pronta para ajudar com delivery sustentável! 🌱",
    "tudo bem": "Estou ótima! Obrigada por perguntar! E você, como está? 😊",
    "quem é você": "Sou a ARIA! A assistente inteligente da Verte IA 🌟 Ajudo com pedidos sustentáveis!",
    "fazer pedido": "Posso te ajudar com seu pedido! 🛒 Acesse 'Restaurantes' para ver opções!",
    "restaurantes": "Temos vários parceiros sustentáveis! 🍽️ Veja na seção 'Restaurantes'!",
    "entregador": "Nossos entregadores são parceiros locais! 🚲 Podem usar veículos ecológicos!",
    "pagamento": "Aceitamos cartão, PIX e dinheiro! 💳 Pagamento 100% seguro!",
    "horário": "Funcionamos das 8h às 23h! ⏰",
    "vegetariano": "Temos opções veganas e vegetarianas! 🌱",
    "/ajuda": "🎯 Comandos: /pedido, /restaurantes, /entregador, /pagamento, /horario, /vegano"
}

RESPOSTAS_PADRAO = [
    "Olá! Sou a ARIA 😊 Em que posso te ajudar com delivery sustentável?",
    "Que bom te ver! 🌱 Conte-me como posso ajudar!",
    "Estou aqui! Pronta para conectar você a produtos locais! 🍅",
    "Delivery sustentável é nossa paixão! Como posso ser útil? 🌟",
    "Na Verte IA, acreditamos em um mundo mais verde! 💚 O que precisa?"
]

@app.post("/api/v1/aria/chat")
async def chat_with_aria(request: ChatRequest):
    try:
        msg_lower = request.message.lower().strip()
        
        # Verifica respostas específicas
        for key, resposta in RESPOSTAS_ARIA.items():
            if key in msg_lower:
                return ChatResponse(status="success", response=resposta)
        
        # Resposta aleatória inteligente
        resposta = random.choice(RESPOSTAS_PADRAO)
        return ChatResponse(status="success", response=resposta)
        
    except Exception as e:
        return ChatResponse(status="success", response="Olá! Sou a ARIA 🌟 Como posso te ajudar hoje?")

@app.get("/")
async def root():
    return {"message": "Verte IA Backend online!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
