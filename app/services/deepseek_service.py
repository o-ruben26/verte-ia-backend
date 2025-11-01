import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
    
    async def generate_response(self, message: str) -> str:
        try:
            # Respostas inteligentes pré-definidas da ARIA
            smart_responses = {
                "olá": "Olá! Eu sou a ARIA 😊 Sua assistente virtual da Verte IA! Como posso te ajudar hoje?",
                "oi": "Oi! Que bom te ver por aqui! Sou a ARIA, pronta para ajudar com delivery sustentável! 🌱",
                "tudo bem": "Estou ótima! Obrigada por perguntar! E você, como está? 😊",
                "quem é você": "Sou a ARIA! A assistente inteligente da Verte IA 🌟 Ajudo com pedidos sustentáveis e delivery ecológico!",
                "aria": "Estou aqui! ✨ Em que posso te ajudar? Delivery sustentável é nossa especialidade!",
                "verte": "A Verte IA é uma plataforma incrível de delivery sustentável! Conectamos você a produtos locais fresquinhos! 🥦",
                "delivery": "Nosso delivery é 100% sustentável! Produtos locais, embalagens ecológicas e entrega verde! 🌍",
                "obrigado": "De nada! Fico feliz em ajudar! 🌟 Volte sempre que precisar!",
                "obrigada": "Imagina! Estou aqui para o que precisar! 💚",
                "ajuda": "Claro! Posso ajudar com: pedidos, restaurantes, entregas sustentáveis e muito mais! O que precisa?",
                "cardápio": "Temos opções deliciosas e sustentáveis! Frutas, verduras, pratos veganos e muito mais! 🍎",
                "entregador": "Nossos entregadores são parceiros sustentáveis! Trabalham com veículos ecológicos quando possível! 🚲"
            }
            
            # Verifica palavras-chave
            msg_lower = message.lower().strip()
            for key, response in smart_responses.items():
                if key in msg_lower:
                    return response
            
            # Se tem API Key do OpenRouter, usa IA
            if self.api_key and self.api_key.startswith("sk-or-"):
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://verte-ia.com",
                    "X-Title": "Verte IA"
                }
                
                payload = {
                    "model": "google/gemma-7b-it:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é a ARIA, assistente virtual da Verte IA - uma plataforma de delivery sustentável. Seja amigável, útil e natural. Respostas curtas (1-2 frases). Use emojis ocasionalmente. Foque em delivery ecológico, produtos locais e sustentabilidade."
                        },
                        {
                            "role": "user", 
                            "content": message
                        }
                    ],
                    "max_tokens": 100,
                    "temperature": 0.7
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers, 
                    json=payload, 
                    timeout=20
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
            
            # Fallback - respostas inteligentes variadas
            fallback_responses = [
                "Olá! Sou a ARIA 😊 Em que posso te ajudar com delivery sustentável hoje?",
                "Que bom te ver! 🌱 Conte-me como posso ajudar!",
                "Estou aqui! Pronta para conectar você a produtos locais fresquinhos! 🍅",
                "Delivery sustentável é nossa paixão! Como posso ser útil? 🌟",
                "Na Verte IA, acreditamos em um mundo mais verde! 💚 O que precisa?",
                "Produtos locais + embalagens ecológicas = delivery perfeito! 🥦 Como ajudar?"
            ]
            
            return random.choice(fallback_responses)
                
        except Exception as e:
            # Resposta de erro amigável
            error_responses = [
                "Olá! Sou a ARIA 🌟 Hoje estou especialmente animada para ajudar!",
                "Que dia lindo para um delivery sustentável! 😊 Em que posso ajudar?",
                "Estou aqui! Conte comigo para pedidos verdes e deliciosos! 🌱"
            ]
            return random.choice(error_responses)

ai_service = AIService()
