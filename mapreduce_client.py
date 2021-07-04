import logging

import grpc

import mapreduce_pb2
import mapreduce_pb2_grpc
  
  
def run():

    channel = grpc.insecure_channel('localhost:50051')
    stub = mapreduce_pb2_grpc.MapReduceStub(channel)
    print("Starting mapping.")
    response = stub.Map(mapreduce_pb2.MapRequest(input_path = 'inputs', output_path='outputs/intermediate', M=4))
    print("Mapping complete. Output files at: " + str(response))
    newpath = str(response.path)
    
    fin = stub.Reduce(mapreduce_pb2.Path(path=newpath))
    if fin.isfinished:
        print("Reduce complete. Final output files at: outputs/out")
        print("Task complete.")
        

if __name__ == '__main__':
    logging.basicConfig()
    run()

