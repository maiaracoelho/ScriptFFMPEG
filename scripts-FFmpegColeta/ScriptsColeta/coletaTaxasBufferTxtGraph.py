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
path_buffer_txt = str(path) + "/txt_buffer"
path_graphs_tx = str(path) + "/graphs_tx"
path_graphs_buffer = str(path) + "/graphs_buffer"
arq.close()

#listar todos os arquivos destes diretorios e colocar em listas
txtLogsBwFiles = os.listdir(path_logsbw_txt)
#txtLogsBwFiles = txtLogsBwFiles.sort()

gplot = Gnuplot.Gnuplot(debug = 1)

for txtLogsBwFile in txtLogsBwFiles:
    txtLogsBfFilewithPath = path_buffer_txt + "/" + txtLogsBwFile
    print txtLogsBfFilewithPath
    title = txtLogsBwFile.split(".")
    title = title[0]
    gplot.title("'"+title+"'")
    #gplot.xlabel('Tempo (s)')
    gplot.ylabel('Buffer Level (s)')
    gplot('set xtics 50')
    gplot('set ytics 10')
    gplot('set grid ytics')
    gplot('set xrange [0:800]')
    gplot('set yrange [0:50]')
    gplot('set t png')
    gplot('set o "'+path_graphs_buffer+'/'+title+'.png"')
    gplot.plot("'"+txtLogsBfFilewithPath+"' u 1:2 w lines t 'Buffer Level (s)'")

for txtLogsBwFile in txtLogsBwFiles:
    txtLogsBwFilewithPath = path_logsbw_txt + "/" + txtLogsBwFile
    txtLogsBrFilewithPath = path_video_txt + "/" + txtLogsBwFile
    print txtLogsBwFilewithPath
    print txtLogsBrFilewithPath
    title = txtLogsBwFile.split(".")
    title = title[0]
    gplot.title("'"+title+"'")
    gplot.xlabel('Time (s)')
    gplot.ylabel('Bandwidth (kb/s)')
    gplot('set ytics ( 300, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 4000)')
    gplot('set xtics 50')
    gplot('set xrange [0:800]')
    gplot('set yrange [100:4500]')
    gplot('set xtics nomirror rotate by -45')

    gplot('set t png')
    gplot('set o "'+path_graphs_tx+'/'+title+'.png"')
    gplot.plot("'"+txtLogsBwFilewithPath+"' u 1:2 w steps t 'Bandwidth Available (kb/s)', '"+txtLogsBrFilewithPath+"'u 1:2 w p t 'Bit Rate (kb/s)'")



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
