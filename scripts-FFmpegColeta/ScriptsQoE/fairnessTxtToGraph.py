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
comand = ""
virg = False

for txtLogsFairtFile in txtLogsFairtFiles:
    txtLogsFairFilewithPath = path_logsfair_txt + "/" + txtLogsFairtFile
    print txtLogsFairFilewithPath
    algo = txtLogsFairtFile.split("_")
    algo = algo[2]
    
    if virg == True:
        comand += ", '"+txtLogsFairFilewithPath+"' u 2:xtic(1) t '"+algo+"'"
    else:
        comand += "'"+txtLogsFairFilewithPath+"' u 2:xtic(1) t '"+algo+"'"
        virg = True

print comand    

gplot.title("Gráfico Comparativo de Justiça entre os Algoritmos")
gplot.ylabel('Justiça')
gplot.xlabel('Algoritmo')
gplot('set ytics 2')
gplot('set grid')
gplot('set t png')
gplot('set style fill pattern')
gplot('set style histogram cluster gap 1')
gplot('set style data histograms')
gplot('set style fill transparent solid 0.4 noborder')
gplot('set xtics nomirror rotate by -45')
gplot('set t png')

gplot('set o "'+path_graphs_fair+'/comparative_fairness.png"')
gplot.plot(comand)
