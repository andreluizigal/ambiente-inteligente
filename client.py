import socket
import protobuf_pb2

HOST = ('localhost', 3001)

def main():
    global HOST

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(HOST)
    except: print("Não foi possível conectar ao Home Assistant")

    requisicao = protobuf_pb2.Request()
    requisicao.device = 99
    requisicao.on = True
    
    cliente.sendto(requisicao.SerializeToString(), HOST)
    

    while True:
        data = cliente.recv(4096)
        resposta = protobuf_pb2.Response()
        resposta.ParseFromString(data)  

        print("\n###########################\n")

        print("Nível de fumaça atual:", resposta.requests[0].value)
        print("Temperatura atual:", resposta.requests[1].value)
        print("Luminosidade atual:", resposta.requests[2].value)
        print("Alarme e combate à incêndio ligado?:", resposta.requests[3].on)
        print("Ar-condicionado ligado?:", resposta.requests[4].on)
        print("Lâmpada ligada?:", resposta.requests[5].on)

        print("\nEscolha um dispositivo para alterar o status:")
        print("1 - Alarme e combate à incêndio")
        print("2 - Ar-condicionado")
        print("3 - Lâmpada")

        d = int(input("Digite o número do dispositivo ou 0 para atualizar a lista: "))
        
        try:
            requisicao.Clear()
            requisicao.device = d + 2
            requisicao.on = not resposta.requests[d+2].on
            cliente.sendto(requisicao.SerializeToString(), HOST)
            print(f"\nStatus do dispositivo {d} alterado!")

        except:
            atualizar = protobuf_pb2.Request()
            atualizar.device = 99
            atualizar.on = True
            cliente.sendto(atualizar.SerializeToString(), HOST)
            continue

if __name__ == "__main__":
    main()

        
        
