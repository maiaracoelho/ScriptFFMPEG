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
path_logsinst_txt = str(path) + "/txt_logsinstability"
path_graphs_inst = str(path) + "/graphs_instability"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsInstFiles = os.listdir(path_logsinst_txt)
#txtLogsBwFiles = txtLogsBwFiles.sort()

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsInstFile in txtLogsInstFiles:
    txtLogsInstFilewithPath = path_logsinst_txt + "/" + txtLogsInstFile
    print txtLogsInstFilewithPath
    title = txtLogsInstFile.split(".")
    title = title[0]
    gplot.title("'Instabilidade'")
    gplot.ylabel('Instabilidade')
    gplot.xlabel('Tempo (s)')
    gplot('set yrange [0:2]')
    gplot('set xrange [0:900]')
    gplot('set xtics 50')
    gplot('set ytics 0.25')
    gplot('set grid ytics')
    gplot('set t png')
    gplot('set xtics nomirror rotate by -45')
    gplot('set t png')

    gplot('set o "'+path_graphs_inst+'/'+title+'.png"')
    gplot.plot("'"+txtLogsInstFilewithPath+"' u 1:2  w l t  'Instabilidade nos 4 últimos seg'")
    