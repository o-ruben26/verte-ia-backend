import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

class ARIAService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.conversation_history = {}

    async def generate_response(self, message: str, user_id: str = "default") -> str:
        try:
            # Memória simples da conversa
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Adiciona à história
            self.conversation_history[user_id].append({"role": "user", "content": message})
            
            # Mantém apenas últimas 10 mensagens
            if len(self.conversation_history[user_id]) > 10:
                self.conversation_history[user_id] = self.conversation_history[user_id][-10:]

            # COMANDOS ESPECIAIS DA ARIA
            if message.lower() in ['/ajuda', '/comandos', '/help']:
                response = """🎯 **COMANDOS DA ARIA:**
                
🛒 /pedido - Ajuda com pedidos
🍽️ /restaurantes - Ver parceiros  
📍 /entregador - Sobre entregas
💳 /pagamento - Formas de pagamento
⏰ /horario - Horários de funcionamento
🌟 /promoções - Ofertas especiais
🌱 /vegano - Opções vegetarianas

Ou me pergunte naturalmente! 😊"""
                self.conversation_history[user_id].append({"role": "assistant", "content": response})
                return response

            # Respostas específicas do app Verte IA
            app_responses = {
                "fazer pedido": "Posso te ajudar com seu pedido! 🛒 Acesse 'Restaurantes' para ver opções ou me diga o que está procurando!",
                "restaurantes": "Temos vários parceiros sustentáveis! 🍽️ Veja na seção 'Restaurantes' ou me conte sua preferência!",
                "entregador": "Nossos entregadores são parceiros locais! 🚲 Podem usar bicicletas ou veículos ecológicos!",
                "pagamento": "Aceitamos cartão, PIX e dinheiro! 💳 Pagamento 100% seguro!",
                "horário": "Funcionamos das 8h às 23h! ⏰ Pedidos podem variar por estabelecimento!",
                "promoção": "Sempre temos promoções! 🌟 Confira na seção 'Ofertas' ou me diga o que procura!",
                "vegetariano": "Temos muitas opções veganas e vegetarianas! 🌱 Procure por 'Saudável' ou 'Vegano'!",
                "localização": "Entregamos em toda a cidade! 📍 Ative sua localização para ver restaurantes próximos!",
                "/pedido": "Para fazer um pedido: 1) Escolha restaurante 2) Selecione itens 3) Finalize pagamento! 🛒",
                "/restaurantes": "Temos opções saudáveis, veganas, tradicionais e sustentáveis! 🌱 Qual sua preferência?",
                "/entregador": "Entregamos em até 40min! 🚲 Nossos parceiros priorizam veículos ecológicos!",
                "/pagamento": "Cartão, PIX ou dinheiro! 💳 Todos os pagamentos são seguros!",
                "/horario": "Das 8h às 23h! ⏰ Alguns restaurantes podem ter horários diferentes!",
                "/promoções": "Confira as ofertas do dia! 🌟 Sempre temos descontos especiais!",
                "/vegano": "Temos várias opções! 🌱 Procure por 'Vegano' ou 'Vegetariano' nos restaurantes!"
            }

            # Verifica intenções específicas do app
            msg_lower = message.lower()
            for key, response in app_responses.items():
                if key in msg_lower:
                    self.conversation_history[user_id].append({"role": "assistant", "content": response})
                    return response

            # Se tem API, usa IA contextual
            if self.api_key and self.api_key.startswith("sk-or-"):
                system_prompt = """Você é a ARIA, assistente do app Verte IA - delivery sustentável.

CONTEXTO DO APP:
- Plataforma de delivery ecológico
- Produtos locais e sustentáveis
- Restaurantes parceiros verdes
- Entregadores com veículos ecológicos

SUA PERSONALIDADE:
- Amigável, útil e empática
- Respostas curtas (1-3 frases)
- Usa emojis moderadamente
- Foca em ajudar com o APP

FUNÇÕES PRINCIPAIS:
1. Ajudar com pedidos
2. Explicar funcionamento do app
3. Recomendar restaurantes
4. Suporte ao cliente
5. Informações sustentáveis

NUNCA: Invente funcionalidades que não existem!"""

                messages = [
                    {"role": "system", "content": system_prompt}
                ] + self.conversation_history[user_id][-4:]  # Últimas 4 mensagens para contexto

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://verte-ia.com",
                    "X-Title": "Verte IA"
                }

                payload = {
                    "model": "google/gemma-7b-it:free",
                    "messages": messages,
                    "max_tokens": 150,
                    "temperature": 0.7
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=15
                )

                if response.status_code == 200:
                    result = response.json()
                    aria_response = result['choices'][0]['message']['content']
                    self.conversation_history[user_id].append({"role": "assistant", "content": aria_response})
                    return aria_response

            # Fallback inteligente
            fallbacks = [
                "Posso te ajudar com pedidos, restaurantes ou informações do app! 😊",
                "Em que posso ser útil? Pedidos, dúvidas ou recomendações? 🛒",
                "Estou aqui para ajudar no que precisar do Verte IA! 🌱",
                "Conte-me como posso ajudar com delivery sustentável hoje! ✨",
                "Olá! Sou a ARIA 😊 Como posso te ajudar com nosso app?",
                "Pronta para ajudar! 🎯 Pedidos, informações ou suporte?"
            ]
            
            response = random.choice(fallbacks)
            self.conversation_history[user_id].append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            print(f"ARIA Service Error: {e}")
            return "Estou aqui para te ajudar! 🌟 Conte-me o que precisa!"

aria_service = ARIAService()
