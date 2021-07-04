import futures3
import threading 
import logging
import re
import os

import grpc

import mapreduce_pb2
import mapreduce_pb2_grpc

def make_output_dirs(output_dir):
    """Makes a directory if it does not already exist."""
    
    if not os.path.isdir(output_dir):
        print("Making output directory at: {}".format(output_dir))
        os.makedirs(output_dir)
    return None

def get_files(path, end):
    """Takes a path and returns a list of the files in that directory that end in end arg (must be string)"""
    
    return [os.path.join(path, os.listdir(path)[i]) for i in range(len(os.listdir(path))) if os.listdir(path)[i].endswith(end)]
       
def map_one_file(path, n, M, output_path):
    
    """Takes a single .txt file and returns buckets of words separated by fractions of M 
    ========== Arguments: ==========
    fpath: string, path to .txt file
    n: int, map task id
    m: int, number of buckets
    ================================
    """
    
    # 0) Initialize buckets and clean words
    buckets = [[] for i in range(M)]                                    
    
    f = open(path, 'rt')                                                
    text = f.read()  
    f.close()
    words = text.split()                                                
    
    # 1) Sort words into buckets
    for word in words:                                                  
        word = re.sub(r'[^\w\s]', '', word)                             # remove punctuation 

        if len(word) > 0:
            letter = word[0]                                            # sort by first letter, also remove non-word strings

            if ord(letter) > 96 and ord(letter) < 123:                  
                buckets[ ord(letter)% M ].append(word.lower())
            else:
                pass 
    
    # 2) Put bucketed words into txt files, save these files in output dir
    output_fname_list = []
    
    for m, bucket in enumerate(buckets):

        output_text = "\n".join(bucket)
        fname_out = os.path.join(output_path, "mr-{}-{}".format(n, m))  # name of file is mr-<map task id>-<reduce task id>

        with open(fname_out, "w") as output:                            # write the txt file and save in the output dir
            output.write(output_text)
        output.close()

        output_fname_list.append(fname_out)

    return '\n'.join(output_fname_list)


def reduce_files(fnames_list, m, output_dir):
    
    """Takes a list of .txt files, pools all the words and performs a word count. Saves in output dir
    ========== Arguments: ==========
    fnames_list: list of strings, full paths to .txt files to reduce 
    m: int, reduce task ID (bucket ID)
    output_dir: string, path to folder in which to save output files
    ================================
    """

    # 1) Aggregate words from same bucket id:
    words_all_buckets = []

    for fname in fnames_list:
        f = open(fname, 'rt')
        text = f.read()
        f.close()
        words = text.split()
        words_all_buckets += words
        
    # 2) Count occurences of unique words:
    words_set = set(words_all_buckets)                                      
    word_count = []
    
    for word in words_set:
        count = words_all_buckets.count(word)
        result = str(word) + " " + str(count)
        word_count.append(result)
    
    word_count_out = "\n".join(word_count)                                  # make a text-friendly string 
    
    # 3) Save output
    fname_out = os.path.join(output_dir, "out-{}".format(m))
    with open(fname_out, "w") as output:
        output.write(word_count_out)
    output.close()
    
    return fname_out


class MapReduceServicer(mapreduce_pb2_grpc.MapReduceServicer):
    """Provides methods that implement functionality of map reduce server."""

    def __init__(self, stop_event):
        self._stop_event = stop_event
        
    def Stop(self, request, context):
        if request.shouldstop:
            self._stop_event.set()
            return mapreduce_pb2.ShutDownResponse(isshutdown = True)
        else:
            pass

    def Map(self, request, context):
        
        self.M = request.M
        
        # Prepare output dir: 
        make_output_dirs(request.output_path)
        
        # Get txt files:
        txt_files = get_files(request.input_path, '.txt')

        # Loop through files and perform mapping function:
        for c, file in enumerate(txt_files):
            out_fname_list = map_one_file(file, c, request.M, request.output_path)
        
            yield mapreduce_pb2.OutputPath(path = out_fname_list)
        
    def Reduce(self, request, context):
        
        # Prepare output dir:
        make_output_dirs(request.output_path)
        
        # Loop through buckets and get corresponding intermediate files 
        for m in range(self.M):
            bucket_files = get_files(request.input_path, str(m))
            
            # Reduce to one file and save in output directory, then report to client
            fname_out = reduce_files(bucket_files, m, request.output_path)
            yield mapreduce_pb2.OutputPath(path = fname_out)
        
    
def serve():
    stop_event = threading.Event() 
    server = grpc.server(futures3.ThreadPoolExecutor(max_workers=10))
    mapreduce_pb2_grpc.add_MapReduceServicer_to_server(
        MapReduceServicer(stop_event), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    stop_event.wait() 
    server.stop(grace = None) 


if __name__ == '__main__':
    logging.basicConfig()
    serve()