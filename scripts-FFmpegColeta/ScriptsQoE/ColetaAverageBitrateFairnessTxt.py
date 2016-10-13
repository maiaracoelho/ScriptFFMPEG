'''
Created on 03/03/2015

@author: Maiara
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
    connection = MySQLdb.connect(host='localhost', user='root', passwd='mysql',db='dash_db5')
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
path, idExecucao1, idExecucao2, idExecucao3, alg, exper = linha.split()
#path_logsfairness_txt = str(path) + "/txt_logsfairness"
#path_logs_txt = str(path) + "/logs"
arq.close()

executions = ["112","113","114", "115", "117", "120"]
#executions = [idExecucao1, idExecucao2, idExecucao3]
#Recuperar todos os throughs de tres sessoes especificas

avaliationTime = 720
#expectResult = 1333 # kbps 1/3 de 4 Mbps baseado na vazao
#expectResult = 2660 # kbps media das taxas do conjunto de videos. Granularidade de 80. Sem taxa de fuga
#expectResult = 2578.518519 # kbps media das taxas do conjunto de videos. Granularidade de 80. Com taxa de fuga
#expectResult = 2660 # kbps media das taxas do conjunto de videos. Granularidade de 400. Sem taxa de fuga
expectResult = 2345.714286 # kbps media das taxas do conjunto de videos. Granularidade de 400. Com taxa de fuga
#expectResult = 1885.714286 # kbps media das taxas do conjunto de videos. Netflix sem fuga
#expectResult = 1568.75 # kbps media das taxas do conjunto de videos. Netflix com fuga
gotResult = 0 # kbps bytes da sessao/tempo da sessao
fairness=0
xiSum = 0
xiSum2 = 0
xiCount = 0
averageBitRateResultSum = 0

#Lista todas as execucoes

#Criar o arquivo txt para gravar o algoritmo e sua justica
#arqLogsTxt = open(path_logs_txt + "/log_fairness.txt" , 'a')   
print "----> Experimento "+exper+"<-----"
#arqLogsTxt.write("----> Experimento "+exper+"<-----"+"\n")   


for execution in executions:
    print "----> Id Execution "+execution+"<-----"
    #arqLogsTxt.write("----> Id Execution "+execution+"<-----"+"\n")   
 
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
    bitrateSum=0
    for i in range(0,len(throughs)):
            
            time = datetime.strptime(throughs[i][2], '%Y-%m-%dT%H:%M:%S.%fZ') 
            deltaTime =  time - inicialTimeSession
            deltaTime = deltaTime.total_seconds()
            
            if deltaTime <= avaliationTime and deltaTime >= 60:
                bytes = float(throughs[i][6]) #bytes 
                duration_segment = float(throughs[i][7]) #duracao do segmento em segundos  
                through = float(throughs[i][9]) + 100 #kbps 
                bytesSum  += bytes
                throughsSum  += through 
                bitrateSum  += (through) * duration_segment
                throughCount += 1

    #averageBitRateResult = bitrateSum/(avaliationTime - 60)     
    averageBitRateResult = throughsSum/throughCount     
    gotResult = throughsSum/throughCount     

    averageBitRateResultSum += averageBitRateResult    
  
    xi = float(expectResult)/float(gotResult)
    xiSum += xi
    xi2 = xi * xi
    xiSum2 += xi2

    xiCount += 1
    
    print "Bytes da Sessao: "+ str(bytesSum)
    print "GotResult em kbps da Sessao: "+ str(gotResult)
    print "Average Bitrate: "+ str(averageBitRateResult)
    print "Xi da Sessao: "+ str(xi)
    print "Xi2 da Sessao: "+ str(xi2)
    print "Segmentos da Sessao: %d" %throughCount 
    
    #arqLogsTxt.write("Bytes da Sessao: "+ str(bytesSum)+"\n")   
    #arqLogsTxt.write("Xi da Sessao: "+ str(xi)+"\n")   
    #arqLogsTxt.write("GotResult em kbps da Sessao: "+ str(gotResult)+"\n")   

fairness =  (xiSum*xiSum)/(xiCount * xiSum2)
averageBitRateResultMedia = averageBitRateResultSum/xiCount
print "-----"
print "xiSum: "+ str(xiSum)
print "xiCount: "+ str(xiCount)
print "Justica: "+ str(fairness)
print "Media BitRate: "+ str(averageBitRateResultMedia)

#arqLogsTxt.write("xiSum: "+ str(xiSum)+"\n")   
#arqLogsTxt.write("Justica: "+ str(fairness)+"\n")   
#arqLogsTxt.close()

#Criar o arquivo txt para gravar o algoritmo e sua justica
#arqLogsFairnessTxt = open(path_logsfairness_txt + "/log_fairness_"+alg+"_ex"+exper+".txt" , 'w')   
#arqLogsFairnessTxt.write(str(alg) + " " + str(fairness) + "\n")   
#arqLogsFairnessTxt.close()


       



