# 📂 Sistema Distribuído de Compartilhamento e Roteamento de Imagens

Este projeto foi desenvolvido para o Seminário #01 da disciplina de Sistemas Distribuídos. Ele implementa uma arquitetura Cliente-Servidor com foco em **Troca de Mensagens (Sockets)** e distribuição de armazenamento, atendendo especificamente aos requisitos do **Tema 07: Pasta de Imagens**.

---

## 🎯 Objetivo do Projeto
O sistema permite que um cliente envie imagens (simulando printscreens) para um servidor central sem utilizar a área de transferência do sistema operacional. Para demonstrar os conceitos de **Distribuição, Escalabilidade e Roteamento**, o Servidor Principal toma **decisões dinâmicas**:

1. **No Upload:** Ao receber uma imagem, o Servidor decide aleatoriamente (50/50) se guardará a imagem em seu próprio armazenamento (Máquina Local) ou se enviará via rede para um Nó Secundário.
2. **No Download:** Ao receber um pedido de imagem, o Servidor verifica onde o arquivo está armazenado e decide de qual máquina fará a leitura para devolver ao cliente.

---

## 🏗️ Arquitetura do Sistema

O projeto é composto por 3 scripts em Python que se comunicam exclusivamente via **Sockets TCP**:

1. **`no_secundario.py` (Armazém Auxiliar)**: Roda silenciosamente escutando a porta `5001`. Representa o disco de uma segunda máquina na rede. Cria e gerencia a `pasta_secundaria`.
2. **`servidor.py` (O Cérebro / Coordenador)**: Escuta a porta `5000`. Recebe as imagens do cliente e aplica a regra de negócio de decidir onde os arquivos serão guardados e de onde serão lidos. Cria e gerencia a `pasta_servidor`.
3. **`cliente.py` (Interface do Usuário)**: Um menu interativo que permite enviar e solicitar imagens enviando os dados em formato binário, sem usar o Ctrl+C/Ctrl+V do sistema.

---

## ⚙️ Configuração para Apresentação em Duas Máquinas

Para apresentar no laboratório cumprindo a regra de "usar duas máquinas", faça o seguinte:

**No Notebook 1 (Ex: Computador da Dupla):**
1. Este computador rodará apenas o `no_secundario.py`.
2. Descubra o IP deste computador na rede Wi-Fi (ex: `192.168.1.15`).
3. Não é preciso alterar nada no código (o `HOST = '0.0.0.0'` já permite conexões externas).

**No Notebook 2 (Ex: Seu Computador):**
1. Este computador rodará o `servidor.py` e o `cliente.py`.
2. Abra o arquivo `servidor.py` e altere a variável `IP_NO_SECUNDARIO` para o IP do Notebook 1.
   * *Ex: `IP_NO_SECUNDARIO = '192.168.1.15'`*
3. O `cliente.py` não precisa ser alterado, pois ele se conectará ao servidor no seu próprio computador (`127.0.0.1`).

*(Nota: Para testar sozinho no mesmo PC antes da apresentação, deixe todos os IPs configurados como `'127.0.0.1'`)*.

---

## 🚀 Ordem de Execução (Passo a Passo)

Para o sistema funcionar, os programas precisam ser iniciados em uma **ordem estrita**. Abra 3 janelas de Terminal (CMD/PowerShell) e execute nesta ordem:

**🖥️ Terminal 1 (Nó Secundário):**
```bash
python no_secundario.py

Saída esperada: [NÓ SECUNDÁRIO] Escutando na porta 5001...

🖥️ Terminal 2 (Servidor Principal):

Bash
python servidor.py
Saída esperada: [SERVIDOR] Escutando na porta 5000...

🖥️ Terminal 3 (Cliente):

Bash
python cliente.py
💻 Testando o Sistema
Após iniciar o cliente.py, um menu interativo será exibido:

Plaintext
1. Enviar Printscreen (Upload)
2. Pedir Imagem (Download)
3. Sair
1. Testando o Roteamento (Upload):
Coloque uma imagem (ex: foto.png) na mesma pasta do script cliente.

Escolha a opção 1 e digite o nome da imagem.

Olhe para o Terminal 2 (Servidor): Você verá a decisão que ele tomou. Ele dirá se guardou na pasta_servidor ou se encaminhou para o Nó Secundário (pasta_secundaria).

Dica: Envie várias fotos diferentes. Como a lógica é aleatória (50%), você verá os arquivos se espalhando entre as duas pastas.

2. Testando a Consulta (Download):
Escolha a opção 2 e digite o nome da imagem que você enviou.

Olhe para o Terminal 2 (Servidor): Ele mostrará sua decisão novamente, informando de onde está puxando a foto (da máquina local ou da máquina secundária).

A imagem será salva no cliente com o prefixo recebido_ (ex: recebido_foto.png).

📚 Tecnologias Utilizadas
Linguagem: Python 3.x

Protocolo de Rede: TCP (Transfer Control Protocol), escolhido para garantir que as imagens não cheguem corrompidas.

Bibliotecas Nativas: socket, os, random (Não requer instalação de dependências extras).