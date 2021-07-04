# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mapreduce_pb2 as mapreduce__pb2


class MapReduceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Map = channel.unary_unary(
                '/mapreduce.MapReduce/Map',
                request_serializer=mapreduce__pb2.MapRequest.SerializeToString,
                response_deserializer=mapreduce__pb2.OutputPath.FromString,
                )
        self.Reduce = channel.unary_unary(
                '/mapreduce.MapReduce/Reduce',
                request_serializer=mapreduce__pb2.ReduceRequest.SerializeToString,
                response_deserializer=mapreduce__pb2.isFinished.FromString,
                )
        self.Stop = channel.unary_unary(
                '/mapreduce.MapReduce/Stop',
                request_serializer=mapreduce__pb2.StopRequest.SerializeToString,
                response_deserializer=mapreduce__pb2.ShutDownResponse.FromString,
                )


class MapReduceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Map(self, request, context):
        """A simple RPC.

        Extracts files from given Path, sorts into buckets, and signals the finish. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Reduce(self, request, context):
        """A simple RPC.

        Extracts files from given Path, does word count, and signals the finish. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Shutdown RPC.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MapReduceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Map': grpc.unary_unary_rpc_method_handler(
                    servicer.Map,
                    request_deserializer=mapreduce__pb2.MapRequest.FromString,
                    response_serializer=mapreduce__pb2.OutputPath.SerializeToString,
            ),
            'Reduce': grpc.unary_unary_rpc_method_handler(
                    servicer.Reduce,
                    request_deserializer=mapreduce__pb2.ReduceRequest.FromString,
                    response_serializer=mapreduce__pb2.isFinished.SerializeToString,
            ),
            'Stop': grpc.unary_unary_rpc_method_handler(
                    servicer.Stop,
                    request_deserializer=mapreduce__pb2.StopRequest.FromString,
                    response_serializer=mapreduce__pb2.ShutDownResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mapreduce.MapReduce', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MapReduce(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Map(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapreduce.MapReduce/Map',
            mapreduce__pb2.MapRequest.SerializeToString,
            mapreduce__pb2.OutputPath.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Reduce(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapreduce.MapReduce/Reduce',
            mapreduce__pb2.ReduceRequest.SerializeToString,
            mapreduce__pb2.isFinished.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapreduce.MapReduce/Stop',
            mapreduce__pb2.StopRequest.SerializeToString,
            mapreduce__pb2.ShutDownResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
