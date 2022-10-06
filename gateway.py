import socket, threading
import mensagens_pb2

HOST = ('localhost', 3000)

resposta = mensagens_pb2.Response()

teste1 = mensagens_pb2.Request()
teste1.tipo = 1
teste1.nome = "teste 1"
teste1.ligado = False

(resposta.requests).append(teste1)


def main():
    global HOST

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.bind(HOST)
    servidor.listen(10)

    cliente, endereco = servidor.accept()
    print("Conexão aceita")

    while True:
        
        receberMensagem(cliente)

def receberMensagem(cliente):
    print("CHEGOU NA FUNÇAO")
    global resposta
    data = cliente.recv(4096)

    mensagem = mensagens_pb2.Request()
    mensagem.ParseFromString(data) 

    print("Enviando...")
    cliente.sendall(resposta.SerializeToString())
    

main()

    



    

