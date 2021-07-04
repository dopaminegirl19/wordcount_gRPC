import logging
import sys

import grpc

import mapreduce_pb2
import mapreduce_pb2_grpc

## === USER INPUT ====
f2inputs = 'inputs'
f2intermediate = 'outputs/intermediate'
f2outputs = 'outputs/out'
M = 4
## ===================
  
def run():

    channel = grpc.insecure_channel('localhost:50051')
    stub = mapreduce_pb2_grpc.MapReduceStub(channel)
    
    # Map:
    print("=== Starting map.")
    print("=== Map files:")
    responses = stub.Map(mapreduce_pb2.MapRequest(
        input_path = f2inputs, 
        output_path = f2intermediate, 
        M=M
        ))
    for response in responses:
        print(response.path)
    
    # Reduce:
    print("=== Map complete. Starting reduce. ")
    print("=== Reduce files:")
    responses = stub.Reduce(mapreduce_pb2.ReduceRequest(
        input_path = f2intermediate, 
        output_path =f2outputs
        ))
    for response in responses:
        print(response.path)
    
    # Terminate:
    print("=== Reduce complete. Final output files at: {}.".format(f2outputs))
    print("=== Task complete. Servers and client will now exit.")
    response = stub.Stop(mapreduce_pb2.StopRequest(shouldstop = True))
    sys.exit(0)
        

if __name__ == '__main__':
    logging.basicConfig()
    run()