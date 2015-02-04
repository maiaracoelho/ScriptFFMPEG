'''
Created on 04/02/2015

@author: dash
'''
#!/usr/bin/env python

import os
import time
import string
import csv
from operator import itemgetter

arq = open("entrada_diretorio_captura.txt","r")
linha = arq.readline()
path, logbw,  idExecucao = linha.split()
path_logsbw = str(path) + "/dash_logs_bw"
path_logsbw_txt = str(path) + "/txt_logbw"
path_video_txt = str(path) + "/txt_video"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsBwFiles = os.listdir(path_logsbw_txt)
txtLogsBrfiles = os.listdir(path_video_txt)

#criar o diretorio dos graficos
pathGraph=path+"/graphs"
os.mkdir(pathGraph) 

os.system()


    
