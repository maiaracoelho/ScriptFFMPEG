'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#this program converts a set of txt files to a set of txt for access graph


import os
import time
import string
import csv
from operator import itemgetter

input_path = "/home/dashclient/Dropbox/Pesquisas_Mestrado/experimentos/testes1_dataset4/logs_client_buffer" #diretorio de logs do buffer de audio e de video

txt_files = os.listdir(input_path)

path_output_txt_graph=input_path+"/"+"log_buffer_graph"
os.mkdir(path_output_txt_graph) #criando diretorio onde ficarao os arquivs csv para fazer os graficos

#pass1
for txt_file in txt_files:
    name = txt_file.split(".")
    
    graph_file_output= name[0]
    print txt_file
    arq_txt=arq=open(input_path+"/"+txt_file,"r")
    linhas = arq_txt.readlines()
    dict_buffer={}
    #pass2
    for linha in linhas:
        linha1 = linha.split()
        time = linha1[1].split(".")
        buffer = linha1[4].split(".") 
        time = int (time[0])
        buffer = int (buffer[0])
        dict_buffer[time] = buffer
    
    dict_buffer = sorted(dict_buffer.items(), key=itemgetter(0))
    print dict_buffer
    
    for_graph_file=graph_file_output+"_graph.txt"
    arq_txt.close()
    with open(path_output_txt_graph+"/"+for_graph_file,'wb') as arq_txt_graph:
        w = csv.writer(arq_txt_graph, delimiter=' ')
        w.writerows(dict_buffer)
            
        print txt_file, for_graph_file
        

    
