'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import MySQLdb
import string
from datetime import datetime, timedelta
import math
import csv
from operator import itemgetter

 
#Conectar ao banco
try:
    connection = MySQLdb.connect(host='localhost', user='root', passwd='mysql',db='dash_db')
except:
    print "Error Connection"

cursor = connection.cursor()
  
try:
    connection.select_db("dash_db")
except:
    print "Error DB Selection"

#Obter o diretorio onde os arquivos txt serao gerados 
arq = open("entrada_diretorio_captura.txt","r")
linha = arq.readline()
path, idExecucao1, idExecucao2, idExecucao3, alg = linha.split()
path_logsfairness_txt = str(path) + "/txt_logsfairness"
arq.close()

#executions = [idExecucao1, idExecucao2, idExecucao3]
#executions = ["59", "63", "64", "66", "69", "70", "72", "73", "75", "77"]
#executions = ["39", "40", "42", "44", "46", "48", "51", "53", "55", "57"]
#executions = ["79", "81", "83", "86", "87", "90", "92", "93", "94", "97"]

#Recuperar todos os throughs de tres sessoes especificas

avaliationTime = 720
#expectResult = 1333 # kbps 1/3 de 4 Mbps baseado na vazao
#expectResult =  # kbps media das taxas do conjunto de videos. Granularidade de 80. Sem taxa de fuga
#expectResult = 781.904761905 # kbps media das taxas do conjunto de videos. Granularidade de 80. Com taxa de fuga
expectResult = 2660 # kbps media das taxas do conjunto de videos. Granularidade de 400. Sem taxa de fuga
#expectResult = 2345.714286 # kbps media das taxas do conjunto de videos. Granularidade de 400. Com taxa de fuga
#expectResult = 1885.714286 # kbps media das taxas do conjunto de videos. Netflix sem fuga
#expectResult = 1681.25 # kbps media das taxas do conjunto de videos. Netflix com fuga
gotResult = 0 # kbps bytes da sessao/tempo da sessao
fairness=0
xiSum = 0
xiSum2 = 0
xiCount = 0
bitrateAverageSum = 0
#Lista todas as execucoes
for execution in executions:
    print "----> Id Execution "+execution+"<-----"
     
    #Recuperar todos os throughputs relacionados a execucao
    cursor.execute ('SELECT * FROM dash_execution WHERE id = %d' %int(execution))
    ex = cursor.fetchone()  
    
    #Recuperar todos os throughputs relacionados a execucao
    cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %int(execution))
    throughs = cursor.fetchall()  
        
    inicialTimeSession = datetime.strptime(throughs[0][2], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    throughCount=0
    throughsSum=0
    bytesSum=0
    durationSegmentSum=0
    for i in range(0,len(throughs)):
            
            time = datetime.strptime(throughs[i][2], '%Y-%m-%dT%H:%M:%S.%fZ') 
            deltaTime =  time - inicialTimeSession
            deltaTime = deltaTime.total_seconds()
            
            if deltaTime <= avaliationTime and deltaTime >= 60:
                bytes = float(throughs[i][6]) #bytes 
                duration_segment = float(throughs[i][7]) #duracao do seg 
                through = float(throughs[i][9]) #kbps 
                durationSegmentSum  += (through + 100.0) * duration_segment
                bytesSum  += bytes
                throughsSum  += through + 100.0
                throughCount += 1

    gotResult = throughsSum/throughCount     
    bitrateAverage = durationSegmentSum/(avaliationTime - 60)    
    bitrateAverageSum += bitrateAverage     
    xi = float(expectResult)/float(gotResult)
    xiSum += xi
    xi2 = xi * xi
    xiSum2 += xi2

    xiCount += 1
    
    print "Bytes da Sessao: "+ str(bytesSum)
    print "GotResult em kbps da Sessao: "+ str(gotResult)
    print "bitrateAverage em kbps da Sessao: "+ str(bitrateAverage)
    print "Xi da Sessao: "+ str(xi)
    print "Xi2 da Sessao: "+ str(xi2)
    print "Segmentos da Sessao: %d" %throughCount 
  
fairness =  (xiSum*xiSum)/(xiCount * xiSum2)
AveregaBR =  bitrateAverageSum/xiCount

print "-----"
print "xiSum: "+ str(xiSum)
print "xiCount: "+ str(xiCount)
print "Justica: "+ str(fairness)
print "AveregaBR: "+ str(AveregaBR)

#Criar o arquivo txt para gravar o algoritmo e sua justica
arqLogsFairnessTxt = open(path_logsfairness_txt + "/log_fairness_"+alg+"_ex6.txt" , 'w')   
arqLogsFairnessTxt.write(str(alg) + " " + str(fairness) + "\n")   
arqLogsFairnessTxt.close()


       



