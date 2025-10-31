import os
import requests
import logging

logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, message: str) -> dict:
        try:
            url = f"{self.base_url}/{self.model}"
            payload = {
                "inputs": f"Human: {message}\nAssistant:",
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                else:
                    text = result.get("generated_text", "")
                return {"success": True, "response": text.strip()}
            elif response.status_code == 503:
                return {"success": False, "error": "Modelo carregando."}
            else:
                return {"success": False, "error": f"Erro: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
