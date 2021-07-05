import logging
import sys
import argparse

import grpc

import mapreduce_pb2
import mapreduce_pb2_grpc

## === USER INPUT ====
parser = argparse.ArgumentParser()

parser.add_argument(
    '--p2inputs',
    default='inputs',
    help='provide an string path to input .txt files'
)
parser.add_argument(
    '--p2intermediate',
    default='outputs/intermediate',
    help='provide an string path where to intermediate output files'
)
parser.add_argument(
    '--p2outputs',
    default='outputs/out',
    help='provide an string path where to save the final output files'
)
parser.add_argument(
    '--M',
    default=4,
    help='how many buckets? (int)'
)

clinput = parser.parse_args()

# p2inputs = 'inputs'
# p2intermediate = 'outputs/intermediate'
# p2outputs = 'outputs/out'
# M = 4
## ===================
  
def run():

    channel = grpc.insecure_channel('localhost:50051')
    stub = mapreduce_pb2_grpc.MapReduceStub(channel)
    
    # Map:
    print("=== Starting map.")
    print("=== Map files:")
    responses = stub.Map(mapreduce_pb2.MapRequest(
        input_path = clinput.p2inputs, 
        output_path = clinput.p2intermediate, 
        M = int(clinput.M)
        ))
    for response in responses:
        print(response.path)
    
    # Reduce:
    print("=== Map complete. Starting reduce. ")
    print("=== Reduce files:")
    responses = stub.Reduce(mapreduce_pb2.ReduceRequest(
        input_path = clinput.p2intermediate, 
        output_path = clinput.p2outputs
        ))
    for response in responses:
        print(response.path)
    
    # Terminate:
    print("=== Reduce complete. Final output files at: {}.".format(clinput.p2outputs))
    print("=== Task complete. Servers and client will now exit.")
    response = stub.Stop(mapreduce_pb2.StopRequest(shouldstop = True))
    sys.exit(0)
        

if __name__ == '__main__':
    logging.basicConfig()
    run()