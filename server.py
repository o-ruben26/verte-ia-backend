from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os

# Porta dinâmica para Railway
PORT = int(os.environ.get('PORT', 9001))

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

    def do_POST(self):
        if self.path == '/cadastro':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                conn = sqlite3.connect('db/verte.db')
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
                
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Not Found'}).encode())

print(f'🚀 Servidor rodando na porta {PORT}')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
