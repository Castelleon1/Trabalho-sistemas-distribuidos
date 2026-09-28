import socket
import os

IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000

def enviar_imagem(caminho_imagem):
    nome_arquivo = os.path.basename(caminho_imagem)
    if not os.path.exists(caminho_imagem):
        print(f"\n[ERRO] Imagem não encontrada.")
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP_SERVIDOR, PORTA_SERVIDOR))
        s.sendall(f'UPLOAD|{nome_arquivo}'.encode('utf-8'))
        s.recv(1024) 
        
        with open(caminho_imagem, 'rb') as f:
            s.sendall(f.read())
        s.shutdown(socket.SHUT_WR)
        
        s.recv(1024)
        print(f'[CLIENTE] Imagem enviada com sucesso!')
    finally:
        s.close()

def baixar_imagem(nome_arquivo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP_SERVIDOR, PORTA_SERVIDOR))
        s.sendall(f'DOWNLOAD|{nome_arquivo}'.encode('utf-8'))
        resposta = s.recv(1024).decode('utf-8')
        
        if resposta == 'OK':
            s.sendall(b'PRONTO')
            caminho_salvar = f"recebido_{nome_arquivo}"
            with open(caminho_salvar, 'wb') as f:
                while True:
                    dados = s.recv(4096)
                    if not dados:
                        break
                    f.write(dados)
            print(f"[CLIENTE] Imagem salva como: {caminho_salvar}")
        else:
            print(f"[CLIENTE] Erro: O arquivo não foi encontrado em nenhuma máquina.")
    finally:
        s.close()

if __name__ == '__main__':
    while True:
        print("\n1. Enviar Printscreen (Upload)\n2. Pedir Imagem (Download)\n3. Sair")
        opcao = input("Escolha: ")
        
        if opcao == '1':
            enviar_imagem(input("Nome da imagem: "))
        elif opcao == '2':
            baixar_imagem(input("Nome da imagem: "))
        elif opcao == '3':
            break