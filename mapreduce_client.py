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
    print("Starting map.")
    response = stub.Map(mapreduce_pb2.MapRequest(
        input_path = f2inputs, 
        output_path = f2intermediate, 
        M=M
        ))
    print("Map complete. Output files at: " + str(response))
    
    # Reduce: 
    print("Starting reduce.")
    fin = stub.Reduce(mapreduce_pb2.ReduceRequest(input_path = response.path, output_path =f2outputs))
    if fin: #fin.isfinished:
        print("Reduce complete. Final output files at: ".format(f2outputs))
        
        # Close server:
        print("Task complete. Closing servers.")
        response = stub.Stop(mapreduce_pb2.StopRequest(shouldstop = True))
        if response.isshutdown:
            print("Servers closed, client will now exit.")
            sys.exit(0)
        

if __name__ == '__main__':
    logging.basicConfig()
    run()

