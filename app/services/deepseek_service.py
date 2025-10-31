import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    async def generate_response(self, message: str) -> str:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é a ARIA, assistente da Verte IA. Seja amigável, prestativa e objetiva. Respostas curtas (2-3 frases)."
                    },
                    {
                        "role": "user", 
                        "content": message
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return "Desculpe, tive um problema técnico. Pode tentar novamente?"
                
        except Exception as e:
            return "Desculpe, estou com problemas de conexão. Tente novamente!"

deepseek_service = DeepSeekService()
