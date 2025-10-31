from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
import time
from anthropic import Anthropic

PORT = int(os.environ.get('PORT', 10000))
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

def get_db():
    """Conexão SQLite com configurações otimizadas"""
    conn = sqlite3.connect('db/verte.db', timeout=30.0, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=30000')
    return conn

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_HEAD(self):
        """Suporte para requisições HEAD (health checks)"""
        self._set_headers()

    def do_GET(self):
        """Suporte para requisições GET (health checks)"""
        if self.path == '/' or self.path == '/health':
            self._set_headers()
            response = {'status': 'ok', 'message': 'Server is running'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Not Found'}).encode())

    def do_POST(self):
        if self.path == '/cadastro':
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    conn = get_db()
                    c = conn.cursor()
                    
                    tipo = data.get('tipo')
                    
                    if tipo == 'cliente':
                        c.execute("INSERT INTO clientes (nome, sobrenome, email, senha) VALUES (?, ?, ?, ?)",
                                 (data['nome'], data['sobrenome'], data['email'], data['senha']))
                        redirect = '/app/home.html'
                        
                    elif tipo == 'parceiro':
                        c.execute("INSERT INTO parceiros (nome, cpf, email, telefone, veiculo, placa) VALUES (?, ?, ?, ?, ?, ?)",
                                 (data['nome'], data['cpf'], data['email'], data['telefone'], data['veiculo'], data.get('placa', '')))
                        redirect = '/miniapps/parceiro.html'
                        
                    elif tipo == 'empreendedor':
                        cpf_cnpj = data.get('cpf') or data.get('cnpj')
                        c.execute("INSERT INTO empreendedores (nome, email, telefone, cnpj, nome_empresa, categoria) VALUES (?, ?, ?, ?, ?, ?)",
                                 (data['nome'], data['email'], data['telefone'], cpf_cnpj, 
                                  data.get('nome_empresa', data['nome']), data['categoria']))
                        redirect = '/miniapps/empreendedor.html'
                    
                    conn.commit()
                    conn.close()
                    
                    self._set_headers()
                    response = {'status': 'success', 'message': 'Cadastro realizado!', 'redirect': redirect}
                    self.wfile.write(json.dumps(response).encode())
                    return
                    
                except sqlite3.OperationalError as e:
                    if 'locked' in str(e) and attempt < max_retries - 1:
                        time.sleep(0.5)
                        continue
                    else:
                        raise
                except Exception as e:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
                    return
                    
        elif self.path == '/aria':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                message = data.get('message', '')
                
                # Verificar se tem API Key
                if not ANTHROPIC_API_KEY:
                    response_text = 'Desculpe, a API do Claude não está configurada. Por favor, configure a variável ANTHROPIC_API_KEY no Render.'
                else:
                    try:
                        # Usar Claude API
                        client = Anthropic(api_key=ANTHROPIC_API_KEY)
                        
                        completion = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1024,
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"""Você é a ARIA, a assistente de voz inteligente da plataforma Verte IA - uma plataforma de delivery sustentável que conecta clientes, parceiros entregadores e empreendedores locais.

Sua personalidade:
- Amigável, prestativa e objetiva
- Responde de forma clara e natural
- Usa linguagem casual mas profissional
- Respostas curtas (máximo 2-3 frases)

Usuário perguntou: {message}

Responda de forma natural e útil:"""
                                }
                            ]
                        )
                        
                        response_text = completion.content[0].text
                        
                    except Exception as e:
                        print(f"Erro na API do Claude: {e}")
                        response_text = f"Desculpe, tive um problema ao processar sua mensagem. Pode tentar novamente?"
                
                self._set_headers()
                response = {'status': 'success', 'response': response_text}
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                print(f"Erro geral: {e}")
                self._set_headers(500)
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
                return
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Not Found'}).encode())

print(f'🚀 Servidor rodando na porta {PORT}')
print(f'🤖 Claude API: {"✅ Configurada" if ANTHROPIC_API_KEY else "❌ Não configurada"}')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
