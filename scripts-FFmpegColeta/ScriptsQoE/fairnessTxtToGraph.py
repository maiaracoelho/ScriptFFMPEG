'''
Created on 04/02/2015

@author: dash
'''
#!/usr/bin/env python

import os
import time
import string
from operator import itemgetter
from os import system, remove
import Gnuplot, Gnuplot.funcutils

arq = open("entrada_diretorio_captura.txt","r")
linha = arq.readline()
path, idExecucao1, idExecucao2, idExecucao3, alg = linha.split()
path_logsfair_txt = str(path) + "/txt_logsfairness"
path_graphs_fair = str(path) + "/comparative_graphs"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsFairtFiles = os.listdir(path_logsfair_txt)

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsFairtFile in txtLogsFairtFiles:
    txtLogsFairFilewithPath = path_logsfair_txt + "/" + txtLogsFairtFile
    print txtLogsFairFilewithPath
