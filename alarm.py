import grpc, protobuf_pb2, protobuf_pb2_grpc
from concurrent import futures

online = False

class TurnServicer(protobuf_pb2_grpc.TurnServicer):
    def TurnOn(self, request, context):
        global online
        online = True
        resp = protobuf_pb2.Status()
        resp.on = True
        arq = open("smoke.txt", "w+")
        arq.write("0")
        arq.close()
        print("Ligou!")
        return resp

    def TurnOff(self, request, context):
        global online
        print("testef: ", request)
        online = False
        resp = protobuf_pb2.Status()
        resp.on = False
        arq = open("smoke.txt", "w+")
        arq.write("100")
        arq.close()
        print("Desligou!")
        return resp

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protobuf_pb2_grpc.add_TurnServicer_to_server(TurnServicer(), server)
    server.add_insecure_port("localhost:50001")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()