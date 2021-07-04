import logging

import grpc

import mapreduce_pb2
import mapreduce_pb2_grpc

## === USER INPUT ====
f2inputs = 'inputs'
f2intermediate = 'outputs/intermediate'
f2outputs = 'outputs/out'
M = 4
  
def run():

    channel = grpc.insecure_channel('localhost:50051')
    stub = mapreduce_pb2_grpc.MapReduceStub(channel)
    
    # Map:
    print("Starting map.")
    response = stub.Map(mapreduce_pb2.MapRequest(
        input_path = f2inputs, 
        output_path = f2outputs, 
        M=M
        ))
    print("Map complete. Output files at: " + str(response))
    
    # Reduce: 
    print("Starting reduce.")
    fin = stub.Reduce(mapreduce_pb2.ReduceRequest(
        input_path = f2intermediate,
        output_path = f2outputs
        ))
    if fin.isfinished:
        print("Reduce complete. Final output files at: outputs/out")
        print("Task complete.")
        

if __name__ == '__main__':
    logging.basicConfig()
    run()

