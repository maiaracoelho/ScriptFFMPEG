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
path, logbw,  idExecucao = linha.split()
path_logspop_txt = str(path) + "/txt_logsprobability"
path_graphs_pop = str(path) + "/graphs_probability"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsPopFiles = os.listdir(path_logspop_txt)
#txtLogsBwFiles = txtLogsBwFiles.sort()

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsPopFile in txtLogsPopFiles:
    txtLogsPopFilewithPath = path_logspop_txt + "/" + txtLogsPopFile
    print txtLogsPopFilewithPath
    title = txtLogsPopFile.split(".")
    title = title[0]
    gplot.title(title)
    gplot.ylabel('Probabilidade (%)')
    gplot.xlabel('Tempo (s)')
    gplot('set yrange [0:150]')
    gplot('set xrange [0:900]')
    gplot('set xtics 50')
    gplot('set ytics 10')
    gplot('set grid ytics')
    gplot('set t png')
    gplot('set xtics nomirror rotate by -45')
    gplot('set t png')

    gplot('set o "'+path_graphs_pop+'/'+title+'.png"')
    gplot.plot("'"+txtLogsPopFilewithPath+"' u 1:2  w l t  'Probabilidade nos 15 últimos s'")
    