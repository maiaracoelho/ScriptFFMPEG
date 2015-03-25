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
path_logsreb_txt = str(path) + "/txt_logsrebuffers"
path_graphs_reb = str(path) + "/graphs_rebuffers"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsRebufFiles = os.listdir(path_logsreb_txt)
#txtLogsBwFiles = txtLogsBwFiles.sort()

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsRebufFile in txtLogsRebufFiles:
    txtLogsRebFilewithPath = path_logsreb_txt + "/" + txtLogsRebufFile
    print txtLogsRebFilewithPath
    title = txtLogsRebufFile.split(".")
    title = title[0]
    gplot.title("'Ocorrências x Durações das Rebufferizações'")
    gplot.ylabel('Ocorrência de Rebufferização')
    gplot.xlabel('Tempo (s)')
    gplot('set ytics 1')
    gplot('set xtics 20')
    gplot('set grid ytics')
    gplot('set t png')
    gplot('set xtics nomirror rotate by -45')
    gplot('set t png')

    gplot('set o "'+path_graphs_reb+'/'+title+'.png"')
    gplot.plot("'"+txtLogsRebFilewithPath+"' u 1:2  w p t  'Ocorrências de Rebufferizações'")
    