import os
import socket

HOST = '0.0.0.0'
PORT = 5001
PASTA_SECUNDARIA = './pasta_secundaria'

if not os.path.exists(PASTA_SECUNDARIA):
    os.makedirs(PASTA_SECUNDARIA)

def iniciar_no():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f'[NÓ SECUNDÁRIO] Escutando na porta {PORT}...')

    try:
        while True:
            conn, endereco = servidor.accept()
            mensagem = conn.recv(1024).decode('utf-8')
            if not mensagem:
                conn.close()
                continue
                
            comando, nome_arquivo = mensagem.split('|')
            caminho_arquivo = os.path.join(PASTA_SECUNDARIA, nome_arquivo)

            if comando == 'UPLOAD':
                conn.sendall(b'OK')
                with open(caminho_arquivo, 'wb') as f:
                    while True:
                        dados = conn.recv(4096)
                        if not dados:
                            break
                        f.write(dados)
                print(f'[NÓ SECUNDÁRIO] Imagem "{nome_arquivo}" guardada aqui.')
                conn.sendall(b'SUCESSO')
                
            elif comando == 'DOWNLOAD':
                if os.path.exists(caminho_arquivo):
                    conn.sendall(b'OK')
                    conn.recv(1024) 
                    with open(caminho_arquivo, 'rb') as f:
                        conn.sendall(f.read())
                    print(f'[NÓ SECUNDÁRIO] Enviando "{nome_arquivo}" de volta ao Servidor.')
                else:
                    conn.sendall(b'ERRO')

            try:
                conn.shutdown(socket.SHUT_WR)
            except OSError:
                pass
            conn.close()
    except KeyboardInterrupt:
        print("\n[NÓ SECUNDÁRIO] Encerrado.")

if __name__ == '__main__':
    iniciar_no() 