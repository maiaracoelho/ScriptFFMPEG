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
path_logsbw = str(path) + "/dash_logs_bw"
path_logsbw_txt = str(path) + "/txt_logbw"
path_video_txt = str(path) + "/txt_video"
path_graphs = str(path) + "/graphs"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsBwFiles = os.listdir(path_logsbw_txt)
#txtLogsBwFiles = txtLogsBwFiles.sort()

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsBwFile in txtLogsBwFiles:
    txtLogsBwFilewithPath = path_logsbw_txt + "/" + txtLogsBwFile
    txtLogsBrFilewithPath = path_video_txt + "/" + txtLogsBwFile
    print txtLogsBwFilewithPath
    print txtLogsBrFilewithPath
    title = txtLogsBwFile.split(".")
    title = title[0]
    gplot.title("'"+title+"'")
    gplot.xlabel('Tempo (s)')
    gplot.ylabel('Largura de Banda (kbps)')
    gplot('set ytics ( 200, 1600, 2200, 2800, 3400, 4000, 5000)')
    gplot('set xtics 90')
    gplot('set xrange [0:900]')
    gplot('set yrange [0:5000]')
    gplot('set t png')
    gplot('set o "'+path_graphs+'/'+title+'.png"')
    gplot.plot("'"+txtLogsBwFilewithPath+"' u 1:2 w steps t 'Largura de Banda (kbps)', '"+txtLogsBrFilewithPath+"'u 1:2 w p t 'Taxa de bits (kbps)'")
   

'''system('set ytics ( 200000, 1600000, 2200000, 2800000, 3400000, 4000000, 5000000)')
system('set xtics 90')
system('set xlabel "Tempo (s)"')
system('set ylabel "(bps)"')
system('set yrange [0:5000000]')
system('set ylabel "(bps)"')


system('gnuplot %s.gp'%(txtLogsBwFile))
system('set t push')
system('set t png')
system('set o %s'%(txtLogsBwFile))
remove(path_graphs+"/"+'%s.gp'%(txtLogsBwFile))'''
