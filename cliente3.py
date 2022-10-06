import socket, threading
import mensagens_pb2

HOST = ('localhost', 3000)

def main():
    global HOST

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(HOST)

    requisicao = mensagens_pb2.Request()
    requisicao.tipo = 0
    requisicao.nome = "testando"

    cliente.sendto(requisicao.SerializeToString(), HOST)
    

    while True:
        data = cliente.recv(4096)
        resposta = mensagens_pb2.Response()
        resposta.ParseFromString(data)   
        

        print("Escolha um dispositivo:")
        contador = 0
        for x in resposta.requests:
            print(contador, "-", x.nome)

        d = int(input("Número: "))

        requisicao.Clear()
        requisicao.CopyFrom(resposta.requests[d])

        print("Nome:", resposta.requests[d].nome)
        if resposta.requests[d].tipo ==1: 
            print("Tipo: Lâmpada")
            if resposta.requests[d].ligado: print("Status: Ligada (True)")
            else: print("Status: Desligado (False)")
            print("------------------------------- \nAções:\n1 - Ligar/Desligar\n0 - Voltar")

        elif resposta.requests[d].tipo ==2: 
            print("Tipo: Termômetro")
            print("Temperatura:", resposta.requests[d].temperatura)
            print("------------------------------- \nAções:\n0 - Voltar")

            
        elif resposta.requests[d].tipo ==3: 
            print("Tipo: Caixa de som")
            print("Volume:", resposta.requests[d].volume)
            print("------------------------------- \nAções:\n1 - Alterar volume\n0 - Voltar")
        
        c = int(input("Número: "))
        if c == 1 and resposta.requests[d].tipo == 1:
            requisicao.ligado = not requisicao.ligado
            cliente.sendto(requisicao.SerializeToString(), HOST)
            print("O status de", requisicao.nome, "foi alterado para:", requisicao.ligado)
        
        elif c == 1 and resposta.requests[d].tipo == 3:
            requisicao.volume = int(input("Digite o novo volume: "))
            cliente.sendto(requisicao.SerializeToString(), HOST)
            print("O volume de", requisicao.nome, "foi alterado para:", requisicao.volume)
            
        
        else:
            print("Voltando para os dispositivos...")
            cliente.sendto(requisicao.SerializeToString(), HOST)

main()

        
        
