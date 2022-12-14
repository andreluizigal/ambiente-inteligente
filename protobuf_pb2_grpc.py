# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import protobuf_pb2 as protobuf__pb2


class TurnStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TurnOn = channel.unary_unary(
                '/protobuf.Turn/TurnOn',
                request_serializer=protobuf__pb2.Vazio.SerializeToString,
                response_deserializer=protobuf__pb2.Status.FromString,
                )
        self.TurnOff = channel.unary_unary(
                '/protobuf.Turn/TurnOff',
                request_serializer=protobuf__pb2.Vazio.SerializeToString,
                response_deserializer=protobuf__pb2.Status.FromString,
                )


class TurnServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TurnOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TurnOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TurnServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TurnOn': grpc.unary_unary_rpc_method_handler(
                    servicer.TurnOn,
                    request_deserializer=protobuf__pb2.Vazio.FromString,
                    response_serializer=protobuf__pb2.Status.SerializeToString,
            ),
            'TurnOff': grpc.unary_unary_rpc_method_handler(
                    servicer.TurnOff,
                    request_deserializer=protobuf__pb2.Vazio.FromString,
                    response_serializer=protobuf__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protobuf.Turn', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Turn(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TurnOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protobuf.Turn/TurnOn',
            protobuf__pb2.Vazio.SerializeToString,
            protobuf__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TurnOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protobuf.Turn/TurnOff',
            protobuf__pb2.Vazio.SerializeToString,
            protobuf__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
