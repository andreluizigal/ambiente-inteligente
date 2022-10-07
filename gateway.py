import socket, threading, time
import mensagens_pb2

HOST = ('localhost', 3000)

MCAST_GRP = '228.0.0.8'
MCAST_PORT = 6789
UNICAST = ('localhost', 4000)

resposta = mensagens_pb2.Response()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    global HOST, MCAST_GRP, MCAST_PORT, UNICAST, servidor

    #servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(HOST)
    servidor.listen(10)
    
    uni = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    uni.bind(UNICAST)
    #unicast.listen(10)

    conexao = threading.Thread(target=conectarCliente, args=[servidor])
    conexao.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    descobrimento = mensagens_pb2.Request()
    descobrimento.tipo = 0
    descobrimento.nome = "inicial"
    sock.sendto(descobrimento.SerializeToString(), (MCAST_GRP, MCAST_PORT))
    print("Descobrimento enviado")
    sock.close()

    while True:
        thread_dispositivos = threading.Thread(target=receberDispositivo, args=[uni])
        thread_dispositivos.start()

def conectarCliente(servidor):
    cliente, endereco = servidor.accept()

    while True:
        receberMensagem(cliente)

def receberMensagem(cliente):
    global MCAST_GRP, MCAST_PORT, resposta, servidor

    try:
        data = cliente.recv(4096)
        mensagem = mensagens_pb2.Request()
        mensagem.ParseFromString(data)
    except:
        conexao = threading.Thread(target=conectarCliente, args=[servidor])
        conexao.start()
        return


    if mensagem.tipo == 0:
        if not resposta.requests:
            resposta_vazia = mensagens_pb2.Response()
            vazio = mensagens_pb2.Request()
            vazio.nome = "Não há dispositivos conectados"
            (resposta_vazia.requests).append(vazio)
            cliente.sendall(resposta_vazia.SerializeToString())

        else: cliente.sendall(resposta.SerializeToString())
    
    else:
        resposta.Clear()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(mensagem.SerializeToString(), (MCAST_GRP, MCAST_PORT))
        sock.close()

        time.sleep(1)
        cliente.sendall(resposta.SerializeToString())

def receberDispositivo(uni):
    global resposta
    data = uni.recv(4096)
    print("Dispositivo recebido")
    mensagem = mensagens_pb2.Request()
    mensagem.ParseFromString(data)
    if mensagem.tipo == 2:
        try:
            (resposta.requests).remove(mensagem)
        except: print("Temperatura em", mensagem.nome, ":", mensagem.temperatura)

    (resposta.requests).append(mensagem)

    print("Lista:", resposta)

main()

    



    

