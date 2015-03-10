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
path_logspop_txt = str(path) + "/txt_logspopularity"
path_graphs_pop = str(path) + "/graphs_popularity"
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
    gplot.title("'Popularidade das Taxas'")
    gplot.ylabel('Popularidade (%)')
    gplot.xlabel('Taxa de bits (bps)')
    gplot('set ytics 10')
    gplot('set grid')
    gplot('set t png')
    gplot('set style fill pattern')
    gplot('set style histogram cluster gap 1')
    gplot('set style data histograms')
    gplot('set style fill transparent solid 0.4 noborder')
    gplot('set xtics nomirror rotate by -45')
    gplot('set t png')

    gplot('set o "'+path_graphs_pop+'/'+title+'.png"')
    gplot.plot("'"+txtLogsPopFilewithPath+"' u 2:xtic(1) t 'Popularidade da Taxa'")
    