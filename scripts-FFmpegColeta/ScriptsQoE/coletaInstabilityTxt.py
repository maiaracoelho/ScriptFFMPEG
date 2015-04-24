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
path, idExecucao, idExecucao2, idExecucao3, alg = linha.split()
path_logsinstability_txt = str(path) + "/txt_logsinstability"
arq.close()

#Limiar minimo do buffer
BMin = 10
avaliationTime = 720

#Recuperar todos os executions
cursor.execute ('SELECT * FROM dash_execution')
executions = cursor.fetchall()

#Lista todas as execucoes
for execution in executions:
    
     # Verifica se a execucao eh de video
     # Se for, lista tanto os throughputs, quanto os niveis de buffer
     
     if execution[4] == "video":
        id_execution = execution[0]
        mpd_peaces = execution[3].split("/")
        #inicialTimeSession = datetime.strptime(execution[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        #Pega a metrica FR
        fr_parameter = mpd_peaces[5]
        print "------>ExecutionId: %d"%id_execution 
        print "FRparameter: %s"%fr_parameter # Pegar FR
        #Recuperar todos os throughputs relacionados a execucao
        cursor.execute ('SELECT id, time, size_seg, duration, quality, bandwidth FROM dash_throughseg WHERE fk_execution = %d' %int(id_execution))
        throughs1 = cursor.fetchall()
        
        inicialTimeSession = datetime.strptime(throughs1[0][1], '%Y-%m-%dT%H:%M:%S.%fZ')

        k = 4
        diference_bitrate = 0
        bitrate_sum = 0
        instability_sum = 0
        
         #Criar o arquivo txt para gravar os tempos de inicio, fim e duracao das rebufferizacoes
        arqLogsInstabilityTxt = open(path_logsinstability_txt + "/log_instability_exec"+str(id_execution)+".txt" , 'w')
        throughCount=0
        for i in range(3,len(throughs1)):
            diference_bitrate = 0
            bitrate_sum = 0
            time = datetime.strptime(throughs1[i][1], '%Y-%m-%dT%H:%M:%S.%fZ') 
            deltaTime =  time - inicialTimeSession
            deltaTime = deltaTime.total_seconds()
            
            if deltaTime <= avaliationTime:
                for d in range(0, k):
                    bitrate =  int(throughs1[i - d][5]) + 100 #float(throughs1[i - d][2])/float(throughs1[i - d][3])
                    last_bitrate = int(throughs1[i - d - 1][5]) + 100 #float(throughs1[i - d - 1][2])/float(throughs1[i - d - 1][3])
                    diference_bitrate +=  abs(bitrate -last_bitrate) * abs(k - d)
                    
                for d in range(0, k):
                    bitrate_sum += (int(throughs1[i - d - 1][5]) + 100) * abs(k - d)
                
                instability = float(diference_bitrate)/float(bitrate_sum)
                instability_sum += instability
           
                #print str(deltaTime) + " " + str(instability)
                arqLogsInstabilityTxt.write(str(deltaTime) + " " + str(instability) + "\n")   
                throughCount += 1
            

               
        instability_average =  instability_sum/(throughCount - k) 
        
        arqLogsInstabilityTxt.close()

        print "Tamanho de through1: %d" %throughCount 
        print "Instability Average: %f" %instability_average
       

