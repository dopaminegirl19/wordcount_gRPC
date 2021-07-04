# A gRPC for word count #

## What does it do? ##
This code takes the path to a folder containing N .txt files containing words, and performs a word count on the pooled words. <br>
The resulting directory looks like this:

```
outputs
└───intermediate
│   │   mr-0-0
│   │   mr-0-1
│   │   mr-0-2
│   │   mr-0-3
│   │   mr-1-0
│   │   mr-1-2
│   │   ...
│   
└───out
│   │   out-0
│   │   out-1
│   │   out-2
│   │   out-3
```
Where the intermediate file names are mr-<map task id>-<reduce task id> and the file output names are out-<reduce task id>. <br>
Each map task id corresponds to an original .txt file, and each reduce task id corresponds to a bucket (M buckets as instructed by the user).<br>
See **Map Task** and **Reduce Task** sections for details.
 
 ## How to run ##
1. First clone the repo:
 ``` git clone https://github.com/dopaminegirl19/wordcount_gRPC.git```
 - You can use the inputs folder provided in the repo, or your own. In the case of the latter, open up  ```mapreduce_client.py``` and update  ```p2inputs``` as the relative path to your desired inputs folder.
 - Similarly, you can specify the desired path to your outputs folder in  ```mapreduce_client.py```.
1. Then ```cd wordcount_gRPC``` or wherever your cloned repo is.
1. Open up a terminal window and start the server:
 ``` python mapreduce_server.py```
1. In another terminal window, start the client:
  ``` python mapreduce_client.py```
1. The server feeds metadata about the process to the client, so in your client terminal you will be informed as the output files are generated and saved. 
 
## Brief overview of code ##
 - This code uses [gRPC.io](https://grpc.io/) which is google's framework for RPC (remote procedure call). 
 -  ```protos/mapreduce.proto``` specifies the data types and structure in the messages conveyed between the client and the server.
 -  ```mapreduce_pb2.py``` and  ```mapreduce_pb2_grpc.py``` are automatically generated scripts which enable interfacing between the client and server, based on the protocol buffer.
 -  ```mapreduce_server.py``` receives the requests from the client, and carries out the processes.
 -  ```mapreduce_client.py``` receives the user input and formulates the request to send to the server. The user inputs are:
   -  ```p2_inputs``` (string) is the relative path to the .txt files to be parsed 
   - ```p2_intermediate``` (string) is the relative path to the folder in which the server should store the intermediate output files.
   - ```p2_final``` (string) is the relative path to the folder in which the server should store the final output files. 
 - In ```example_outputs``` you can see what the output is if you run the code as is. 
 
 ### Map Task ###
 The map task is called with a MapRequest, consisting of:
 1. ```input_path``` (string), relative path to folder containing .txt files to parse
 1. ```output_path``` (string), relative path to folder containing intermediate output files
 1. ```M``` (int32), number of buckets <br>

 The map task is carried out by the server. The server takes the input files from ```MapRequest.input_path```, separates text into single words, and puts each word into a "bucket" (intermediate file). The bucket is decided by (first letter of the word) % ```MapRequest.M```. Thus, a total of ```M``` * number of .txt files are produced, and each have one word on each line.<br>
 These intermediate files are saved in the specified ```Maprequest.output_path```.<br>
 
The map task returns a ```stream``` of output file names, which are displayed to the user as they are saved. This is because in theory there could be a great many input .txt files to parse, so this way the user can follow the progress of the server. 
 
 ### Reduce Task ###
 The reduce task is called with a ReduceRequest, consisting of:
 1. ```input_path``` (string), relative path to folder containing intermediate files to parse
 1. ```output_path``` (string), relative path to folder containing output files
 
 The reduce task is carried out by the server. The server takes the input files from ```ReduceRequest.input_path```, pools words from buckets with the same id, and counts the occurence of each word. Thus, a total of M files are produced (M is attributed to the server during the map task), and each have one word on each line, followed by its frequency across all the original .txt files.<br>
 These final output files are saved in the specified```ReduceRequest.output_path```.<br>
 
 As in the map task, the reduce task returns a ```stream``` of output file names, which are displayed to the user as they are saved. 
 
 
