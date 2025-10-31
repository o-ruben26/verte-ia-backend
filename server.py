from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
import time

PORT = int(os.environ.get('PORT', 10000))

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
                
                message = data.get('message', '').lower()
                
                # Respostas da ARIA (você pode conectar com IA depois)
                responses = {
                    'olá': 'Olá! Eu sou a ARIA, sua assistente virtual da Verte IA. Como posso ajudar você hoje?',
                    'oi': 'Oi! Tudo bem? Eu sou a ARIA. O que você gostaria de saber?',
                    'quem é você': 'Eu sou a ARIA, a assistente de voz inteligente da plataforma Verte IA. Fui criada para ajudar você a navegar e usar nossos serviços de forma mais fácil e natural.',
                    'ajuda': 'Claro! Posso te ajudar com cadastros, busca de lojas, informações sobre parceiros e muito mais. O que você precisa?',
                    'obrigado': 'Por nada! Estou sempre aqui para ajudar. Volte sempre que precisar!',
                    'tchau': 'Até logo! Foi um prazer ajudar você. Volte sempre que quiser!',
                }
                
                # Procurar resposta
                response_text = None
                for key in responses:
                    if key in message:
                        response_text = responses[key]
                        break
                
                if not response_text:
                    response_text = 'Desculpe, não entendi muito bem. Pode reformular sua pergunta? Estou aqui para ajudar com informações sobre a Verte IA!'
                
                self._set_headers()
                response = {'status': 'success', 'response': response_text}
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
                return
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Not Found'}).encode())

print(f'🚀 Servidor rodando na porta {PORT}')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
