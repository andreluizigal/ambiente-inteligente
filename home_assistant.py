import threading, socket, pika, protobuf_pb2, grpc, protobuf_pb2_grpc

smoke = None
temperature = None
luminosity = None

HOST = ('localhost', 3001)

resposta = protobuf_pb2.Response()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    global HOST, servidor

    servidor.bind(HOST)
    servidor.listen(10)

    print("Servidor ligado!")

    smoke_thread = threading.Thread(target=smoke_sensor_recive, args=[])
    smoke_thread.start()

    temperature_thread = threading.Thread(target=temperature_sensor_recive, args=[])
    temperature_thread.start()

    luminosity_thread = threading.Thread(target=luminosity_sensor_recive, args=[])
    luminosity_thread.start()
    
    conectarCliente(servidor)


def conectarCliente(servidor):
    cliente, endereco = servidor.accept()

    while True:
        receberMensagem(cliente)

def receberMensagem(cliente):
    global resposta, servidor, luminosity, temperature, smoke

    try:
        data = cliente.recv(4096)
        mensagem = protobuf_pb2.Request()
        mensagem.ParseFromString(data)

    except:
        conexao = threading.Thread(target=conectarCliente, args=[servidor])
        conexao.start()
        return

    
    try: status_atuais = [resposta.requests[3].on, resposta.requests[4].on, resposta.requests[5].on]
    except: status_atuais = [False, False, False]
    
    resposta.Clear()

    smoke_sensor = protobuf_pb2.Request()
    smoke_sensor.device = 0
    try: smoke_sensor.value = smoke
    except: smoke_sensor.value = -1
    resposta.requests.append(smoke_sensor)

    temperature_sensor = protobuf_pb2.Request()
    temperature_sensor.device = 1
    try: temperature_sensor.value = temperature
    except: temperature_sensor.value = -1
    resposta.requests.append(temperature_sensor)

    luminosity_sensor = protobuf_pb2.Request()
    luminosity_sensor.device = 2
    try: luminosity_sensor.value = luminosity
    except: luminosity_sensor.value = -1
    resposta.requests.append(luminosity_sensor)

    alarm = protobuf_pb2.Request()
    alarm.device = 3
    alarm.on = status_atuais[0]
    if mensagem.device == 3: alarm.on = alarm_grpc(mensagem.on)
    resposta.requests.append(alarm)

    air_conditioner = protobuf_pb2.Request()
    air_conditioner.device = 4
    air_conditioner.on = status_atuais[1]
    if mensagem.device == 4: air_conditioner.on = air_conditioner_grpc(mensagem.on)
    resposta.requests.append(air_conditioner)

    lamp = protobuf_pb2.Request()
    lamp.device = 5
    lamp.on = status_atuais[2]
    if mensagem.device == 5: lamp.on = lamp_grpc(mensagem.on)
    resposta.requests.append(lamp)

    cliente.sendall(resposta.SerializeToString())


# SMOKE
def smoke_sensor_recive():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('smoke', exclusive=True)
    queue_name = result.method.queue

    binding_key = 'smoke'

    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    channel.basic_consume(
        queue=queue_name, on_message_callback=smoke_callback, auto_ack=True)

    channel.start_consuming()

def alarm_grpc(on):
    with grpc.insecure_channel('localhost:50001') as alarm_channel:
        alarm_stub = protobuf_pb2_grpc.TurnStub(alarm_channel)
        print("alarm_grpc", on)
        if on: 
            resp = alarm_stub.TurnOn(protobuf_pb2.Vazio())
            print("true", resp)
            return resp.on
        else: 
            resp = alarm_stub.TurnOff(protobuf_pb2.Vazio())
            print("false", resp)
            return resp.on


def smoke_callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        global smoke
        smoke = int(body.decode())

# TEMPERATURE
def temperature_sensor_recive():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('temperature', exclusive=True)
    queue_name = result.method.queue

    binding_key = 'temperature'

    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    channel.basic_consume(
        queue=queue_name, on_message_callback=temperature_callback, auto_ack=True)

    channel.start_consuming()


def temperature_callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        global temperature
        temperature = int(body.decode())

def air_conditioner_grpc(on):
    with grpc.insecure_channel('localhost:50002') as air_conditioner_channel:
        air_conditioner_stub = protobuf_pb2_grpc.TurnStub(air_conditioner_channel)
        print("air_conditioner_grpc", on)
        if on: 
            resp = air_conditioner_stub.TurnOn(protobuf_pb2.Vazio())
            print("true", resp)
            return resp.on
        else: 
            resp = air_conditioner_stub.TurnOff(protobuf_pb2.Vazio())
            print("false", resp)
            return resp.on

# LUMINOSITY
def luminosity_sensor_recive():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('luminosity', exclusive=True)
    queue_name = result.method.queue

    binding_key = 'luminosity'

    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    channel.basic_consume(
        queue=queue_name, on_message_callback=luminosity_callback, auto_ack=True)

    channel.start_consuming()


def luminosity_callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        global luminosity
        luminosity = int(body.decode())

def lamp_grpc(on):
    with grpc.insecure_channel('localhost:50003') as lamp_channel:
        lamp_stub = protobuf_pb2_grpc.TurnStub(lamp_channel)
        print("lamp_grpc", on)
        if on: 
            resp = lamp_stub.TurnOn(protobuf_pb2.Vazio())
            print("true", resp)
            return resp.on
        else: 
            resp = lamp_stub.TurnOff(protobuf_pb2.Vazio())
            print("false", resp)
            return resp.on


if __name__ == "__main__":
    main()