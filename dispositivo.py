import socket, time, threading, struct
import mensagens_pb2

MCAST_GRP = '228.0.0.8'
MCAST_PORT = 6789
UNICAST = ('localhost', 4000)


dispositivo = mensagens_pb2.Request()

def main():
    global dispositivo, UNICAST, MCAST_GRP, MCAST_PORT

    print("Criando um novo dispositivo...")
    tipo = int(input("Tipo de dispositivo: \n1 - Lâmpada\n2 - Termometro\n3 - Caixa de som\n"))
    nome = input("Nome do dispositivo: ")

    dispositivo.tipo = tipo
    dispositivo.nome = nome
    #Default
    dispositivo.ligado = False
    if dispositivo.tipo == 3:
        dispositivo.volume = int(input("Volume atual: "))
    if dispositivo.tipo == 2:
        dispositivo.temperatura = float(input("Temperatura atual: "))
        thread_termometro = threading.Thread(target=sensorContinuo)
        thread_termometro.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.sendto(dispositivo.SerializeToString(), UNICAST)
    print("Enviando para o gateway")
    sock.close()

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        data, endereco = sock.recvfrom(4096)
        mensagem = mensagens_pb2.Request()
        mensagem.ParseFromString(data)

        if mensagem.tipo == dispositivo.tipo and mensagem.nome == dispositivo.nome:
            dispositivo.CopyFrom(mensagem)
        sock.sendto(dispositivo.SerializeToString(), UNICAST)

        sock.close()

def sensorContinuo():
    global dispositivo, UNICAST, MCAST_PORT, MCAST_GRP
    while True:
        time.sleep(5)

        sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sockt.sendto(dispositivo.SerializeToString(), UNICAST)
        print("Temperatura enviada")
        
        sockt.close()


main()



    