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
        
def get_txt_files(path):
    """Takes a path and returns a list of the files in that directory that end in .txt"""
    
    return [os.path.join(path, os.listdir(path)[i]) for i in range(len(os.listdir(path))) if os.listdir(path)[i].endswith('.txt')]

def get_bucket_files(path, m):
    """Takes a path and returns a list of the files in that directory that end in m"""
    
    return [os.path.join(path, os.listdir(path)[i]) for i in range(len(os.listdir(path))) if os.listdir(path)[i][-1] == str(m)]
        
def map_one_file(path, n, M, output_path):
    
    """Takes a single .txt file and returns buckets of words separated by fractions of M 
    ========== Arguments: ==========
    fpath: string, path to .txt file
    n: int, map task id
    m: int, number of buckets
    ================================
    """
    
    # 0) Initialize buckets and clean words
    buckets = [[] for i in range(M)]                                    # initialize list of lists for buckets
    
    f = open(path, 'rt')                                                # open file
    text = f.read()                                                     # get text
    words = text.split()                                                # split to get words 
    
    # 1) Sort words into buckets
    for word in words:                                                  # now loop through words
        word = re.sub(r'[^\w\s]', '', word)                             # remove punctuation 

        if len(word) > 0:
            letter = word[0]                                            # sort by first letter, also remove non-word strings

            if ord(letter) > 96 and ord(letter) < 123:                  # remove non-word srtings
                buckets[ ord(letter)% M ].append(word.lower())          # add to bucket and standardize 
            else:
                pass                                                    # pass if not a word 
    
    # 2) Put bucketed words into txt files, save these files in output dir
    
    output_fname_list = []
    
    for m, bucket in enumerate(buckets):                                # buckets filled; now save them in txt files in the intermediate folder 

        output_text = "\n".join(bucket)                                 # arrange words in a list
        fname_out = os.path.join(output_path, "mr-{}-{}".format(n, m))  # name of file is mr-<map task id>-<reduce task id>

        with open(fname_out, "w") as output:                            # write the txt file and save in the output dir
            output.write(output_text)
        output.close()

        output_fname_list.append(fname_out)                             # keep a list of the output txt files to return to the client 

    return output_fname_list


def reduce_files(fnames_list, m, output_dir):
    
    """Takes a list of .txt files, pools all the words and performs a word count. Saves in output dir
    ========== Arguments: ==========
    fnames_list: list of strings, full paths to .txt files to reduce 
    m: int, reduce task ID (bucket ID)
    output_dir: string, path to folder in which to save output files
    ================================
    """

    words_all_buckets = []

    for fname in fnames_list:
        f = open(fname, 'rt')                                               # open file
        text = f.read()                                                     # get text
        words = text.split()                                                # split to get words
        words_all_buckets += words                                          # aggregate words from multiple buckets 
        
    words_set = set(words_all_buckets)                                      # unique words
    word_count = []
    
    for word in words_set:
        count = words_all_buckets.count(word)                                           # count word occurences and format 
        result = str(word) + " " + str(count)
        word_count.append(result)
    
    word_count_out = "\n".join(word_count)                                  # make a text-friendly string 
    
    fname_out = os.path.join(output_dir, "out-{}".format(m))
    with open(fname_out, "w") as output:
        output.write(word_count_out)
    output.close()
    
    return fname_out


class MapReduceServicer(mapreduce_pb2_grpc.MapReduceServicer):
    """Provides methods that implement functionality of map reduce server."""

    def __init__(self):
        self.M = 4                                                  # number of buckets 
        self.intermediate_output_dir = "outputs/intermediate"           # output dir for intermediate outputs (after mapping)
        self.final_output_dir = "outputs/out"                           # output dir for final outputs (after reduce)

    def Map(self, request, context):
        
        # Prepare output dir: 
        # make_output_dirs(self.intermediate_output_dir)
        make_output_dirs(request.output_path)
        
        # Get txt files:
        txt_files = get_txt_files(request.input_path)

        # Loop through files and perform mapping function:
        for c, file in enumerate(txt_files):
            #output_fname_list = map_one_file(file, c, self.M, self.intermediate_output_dir)
            output_fname_list = map_one_file(file, c, request.M, request.output_path)
        
        # Flag finished: 
        return mapreduce_pb2.OutputPath(path="outputs/intermediate")
        
    def Reduce(self, request, context):
        
        # Prepare output dir:
        make_output_dirs(self.final_output_dir)
        
        # Loop through buckets and get corresponding intermediate files 
        for m in range(self.M):
            bucket_files = get_bucket_files(request.path, m)
            
            # Reduce to one file and save in output directory 
            fname_out = reduce_files(bucket_files, m, self.final_output_dir)
        
        
        # Flag finished: 
        return mapreduce_pb2.isFinished(isfinished = True)
    
def serve():
    server = grpc.server(futures3.ThreadPoolExecutor(max_workers=10))
    mapreduce_pb2_grpc.add_MapReduceServicer_to_server(
        MapReduceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()