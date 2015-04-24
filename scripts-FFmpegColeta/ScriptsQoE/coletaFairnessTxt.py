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
    connection = MySQLdb.connect(host='localhost', user='root', passwd='mysql',db='dash_db_fase1')
except:
    print "Error Connection"

cursor = connection.cursor()
  
try:
    connection.select_db("dash_db_fase1")
except:
    print "Error DB Selection"

#Obter o diretorio onde os arquivos txt serao gerados 
arq = open("entrada_diretorio_captura.txt","r")
linha = arq.readline()
path, idExecucao1, idExecucao2, idExecucao3, alg = linha.split()
path_logsfairness_txt = str(path) + "/txt_logsfairness"
arq.close()

executions = [idExecucao1, idExecucao2, idExecucao3]
#Recuperar todos os throughs de tres sessoes especificas

avaliationTime = 720
#expectResult = 1333 # kbps 1/3 de 4 Mbps baseado na vazao
#expectResult = 781.904761905 # kbps 1/3 de 2345,714285714, baseada na media das taxas do conjunto de videos. Granularidade de 80. Sem taxa de fuga
#expectResult = 781.904761905 # kbps 1/3 de 2345,714285714, baseada na media das taxas do conjunto de videos. Granularidade de 80. Com taxa de fuga
#expectResult = 781.904761905 # kbps 1/3 de 2345,714285714, baseada na media das taxas do conjunto de videos. Granularidade de 400. Sem taxa de fuga
expectResult = 781.904761905 # kbps 1/3 de 2345,714285714, baseada na media das taxas do conjunto de videos. Granularidade de 400. Com taxa de fuga
gotResult = 0 # kbps bytes da sessao/tempo da sessao
fairness=0
xiSum = 0
xiSum2 = 0
xiCount = 0
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
    for i in range(0,len(throughs)):
            
            time = datetime.strptime(throughs[i][2], '%Y-%m-%dT%H:%M:%S.%fZ') 
            deltaTime =  time - inicialTimeSession
            deltaTime = deltaTime.total_seconds()
            
            if deltaTime <= avaliationTime:
                bytes = float(throughs[i][6]) #bytes 
                through = float(throughs[i][9]) #kbps 
                bytesSum  += bytes
                throughsSum  += through + 100
                throughCount += 1

    gotResult = throughsSum/throughCount     
    xi = float(expectResult)/float(gotResult)
    xiSum += xi
    xi2 = xi * xi
    xiSum2 += xi2

    xiCount += 1
    
    print "Bytes da Sessao: "+ str(bytesSum)
    print "GotResult em kbps da Sessao: "+ str(gotResult)
    print "Xi da Sessao: "+ str(xi)
    print "Xi2 da Sessao: "+ str(xi2)
    print "Segmentos da Sessao: %d" %throughCount 
  
fairness =  (xiSum*xiSum)/(xiCount * xiSum2)

print "-----"
print "xiSum: "+ str(xiSum)
print "xiCount: "+ str(xiCount)
print "Justica: "+ str(fairness)

#Criar o arquivo txt para gravar o algoritmo e sua justica
arqLogsFairnessTxt = open(path_logsfairness_txt + "/log_fairness_"+alg+"_ex"+str(idExecucao1)+"-"+str(idExecucao2)+"-"+str(idExecucao3)+".txt" , 'w')   
arqLogsFairnessTxt.write(str(alg) + " " + str(fairness) + "\n")   
arqLogsFairnessTxt.close()


       



