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

arq = open("entrada_shared.txt","r")
linha = arq.readline()
path, fileLog, file1, file2, file3,  idExecucao1, idExecucao2, idExecucao3 = linha.split()
path_logsbw = str(path) + "/dash_logs_bw"
path_logsbw_txt = str(path) + "/txt_logbw"
path_video_txt = str(path) + "/txt_video"
path_buffer_txt = str(path) + "/txt_buffer"
path_graphs_tx = str(path) + "/graphs_tx"
path_graphs_buffer = str(path) + "/graphs_buffer"
arq.close()

#Arquivo de Bw
txtLogsBwFile = path_logsbw_txt + "/" + fileLog
#Arquivos de bitsrates
txtLogTxFiles = "'"+path_video_txt + "/" + file1 + "' u 1:2 w lines t 'Player 1', '" + path_video_txt + "/" + file2 +"' u 1:2 w lines t 'Player 2', '"+ path_video_txt + "/" + file3 +"' u 1:2 w lines t 'Player 3'"
#Arquivos de buffer
txtLogBfFiles = "'"+path_buffer_txt + "/" + file1 + "' u 1:2 w lines t 'Player 1', '" + path_buffer_txt + "/" + file2 +"' u 1:2 w lines t 'Player 2', '"+ path_buffer_txt + "/" + file3 + "' u 1:2 w lines t 'Player 3'"

gplot = Gnuplot.Gnuplot(debug = 1)

#grafico de buffer
#title = txtLogsBwFile.split(".")
title = "buffer_graph_execs"+idExecucao1 +"-"+idExecucao2+"-"+idExecucao3
#gplot.title("'"+title+"'")
gplot.xlabel('Tempo (s)')
gplot.ylabel('Ocupação do Buffer (s)')
gplot('set xtics 50')
gplot('set ytics 10')
gplot('set grid ytics')
gplot('set xrange [0:720]')
gplot('set yrange [0:50]')
gplot('set t png')
gplot('set o "'+path_graphs_buffer+'/'+title+'.png"')
gplot.plot(txtLogBfFiles)

#grafico de taxas
print txtLogsBwFile
#title = txtLogsBwFile.split(".")
title = "bitrate_graph_execs"+idExecucao1 +"-"+idExecucao2+"-"+idExecucao3
#gplot.title("'"+title+"'")
gplot.xlabel('Tempo (s)')
gplot.ylabel('Taxas de Bits (kbps)')
gplot('set ytics ( 460, 1660, 2060, 2460, 2860, 3260, 3660, 4000, 5000)')
gplot('set xtics 50')
gplot('set xrange [0:720]')
gplot('set yrange [200:5000]')
gplot('set xtics nomirror rotate by -45')

gplot('set t png')
gplot('set o "'+path_graphs_tx+'/'+title+'.png"')
gplot.plot("'"+txtLogsBwFile+"' u 1:2 w steps t 'Largura de Banda (kbps)',"+txtLogTxFiles)
    