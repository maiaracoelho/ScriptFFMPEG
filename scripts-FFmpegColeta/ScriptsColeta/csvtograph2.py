'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#this program converts a set of csv files to a set of txt for access graph
#1. read csv files into a list
#2. read the list and extract its attributes (bitrate and time)
# 2.1 use the split function to extraction
# 2.2 dont forget to exclude the mpd file and to sum the sintelA bitrate

import os
import time
import string
import csv
from operator import itemgetter

arq=open("entrada_diretorio_captura.txt","r")

input_path = arq.readline()

input_path = input_path.rstrip()
input_path2 = input_path+"csv_files"

csv_files = os.listdir(input_path2)

path_output_csv_graph=input_path+"/"+"csvs_graph2"
os.mkdir(path_output_csv_graph) #criando diretorio onde ficarao os arquivs csv para fazer os graficos

#pass1
for csv_file in csv_files:
    name = csv_file.split(".")
    
    graph_file_output= name[0]
    
    arq_csv=csv.reader(open(input_path2+"/"+csv_file,"rb"))
    bitrates_list=[]
    times_cont=0
    dict_bitrates={}
    #pass2
    for [id, time, url, src, dst] in arq_csv:
        
        url =url.split("_") 
        if url[1]=="sintelV": #eh video
            bitrate = int(url[2])+100
            time, time_r = time.split(".")
            time = int (time)
            dict_bitrates[time] = bitrate   
        

    dict_bitrates = sorted(dict_bitrates.items(), key=itemgetter(0))
    print dict_bitrates
    
    for_graph_file=graph_file_output+"_graph.txt"
     
    with open(path_output_csv_graph+"/"+for_graph_file,'wb') as arq_csv_graph:
        w = csv.writer(arq_csv_graph, delimiter=' ')
        w.writerows(dict_bitrates)
            
        print csv_file, for_graph_file
        
arq.close()

    
