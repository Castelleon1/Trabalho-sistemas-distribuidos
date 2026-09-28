import os
import socket
import random

HOST = '0.0.0.0'
PORT = 5000
PASTA_SERVIDOR = './pasta_servidor'

IP_NO_SECUNDARIO = '127.0.0.1'
PORTA_NO_SECUNDARIO = 5001

if not os.path.exists(PASTA_SERVIDOR):
    os.makedirs(PASTA_SERVIDOR)

def transferir_para_no(nome_arquivo, conteudo):
    """Envia a imagem para ser guardada no Nó Secundário."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_NO_SECUNDARIO, PORTA_NO_SECUNDARIO))
    s.sendall(f'UPLOAD|{nome_arquivo}'.encode('utf-8'))
    s.recv(1024)
    s.sendall(conteudo)
    s.shutdown(socket.SHUT_WR)
    s.recv(1024)
    s.close()

def buscar_no_secundario(nome_arquivo):
    """Busca a imagem na máquina secundária."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_NO_SECUNDARIO, PORTA_NO_SECUNDARIO))
    s.sendall(f'DOWNLOAD|{nome_arquivo}'.encode('utf-8'))
    resposta = s.recv(1024).decode('utf-8')
    if resposta == 'OK':
        s.sendall(b'PRONTO')
        conteudo = bytearray()
        while True:
            dados = s.recv(4096)
            if not dados:
                break
            conteudo.extend(dados)
        s.close()
        return bytes(conteudo)
    s.close()
    return None

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f'[SERVIDOR] Escutando na porta {PORT}...')

    try:
        while True:
            conn, endereco = servidor.accept()
            mensagem = conn.recv(1024).decode('utf-8')
            if not mensagem:
                conn.close()
                continue

            comando, nome_arquivo = mensagem.split('|')

            if comando == 'UPLOAD':
                conn.sendall(b'OK')
                conteudo = bytearray()
                while True:
                    dados = conn.recv(4096)
                    if not dados:
                        break
                    conteudo.extend(dados)

                # CONTEXTO DE DECISÃO NO UPLOAD: Onde guardar?
                decisao_salvar = random.choice(['MÁQUINA_LOCAL', 'MÁQUINA_SECUNDÁRIA'])
                
                if decisao_salvar == 'MÁQUINA_LOCAL':
                    caminho = os.path.join(PASTA_SERVIDOR, nome_arquivo)
                    with open(caminho, 'wb') as f:
                        f.write(conteudo)
                    print(f'[SERVIDOR] Decisão: Guardei "{nome_arquivo}" na minha própria pasta.')
                else:
                    transferir_para_no(nome_arquivo, bytes(conteudo))
                    print(f'[SERVIDOR] Decisão: Mandei "{nome_arquivo}" para a máquina secundária.')
                
                conn.sendall(b'SUCESSO')

            elif comando == 'DOWNLOAD':
                # CONTEXTO DE DECISÃO NO DOWNLOAD: De qual máquina obter?
                caminho_local = os.path.join(PASTA_SERVIDOR, nome_arquivo)
                
                if os.path.exists(caminho_local):
                    print(f'[SERVIDOR] Decisão: A imagem "{nome_arquivo}" está comigo. Obtendo da MÁQUINA LOCAL.')
                    with open(caminho_local, 'rb') as f:
                        arquivo_bytes = f.read()
                else:
                    print(f'[SERVIDOR] Decisão: A imagem "{nome_arquivo}" não está aqui. Obtendo da MÁQUINA SECUNDÁRIA.')
                    arquivo_bytes = buscar_no_secundario(nome_arquivo)

                if arquivo_bytes:
                    conn.sendall(b'OK')
                    conn.recv(1024)
                    conn.sendall(arquivo_bytes)
                else:
                    conn.sendall(b'ERRO')

            try:
                conn.shutdown(socket.SHUT_WR)
            except OSError:
                pass
            conn.close()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Encerrado.")

if __name__ == '__main__':
    iniciar_servidor()