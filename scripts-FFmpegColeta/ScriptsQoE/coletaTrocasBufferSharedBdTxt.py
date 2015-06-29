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
path, idExecucao, idExecucao2, idExecucao3, alg, exper = linha.split()
path_logsrebuffers_txt = str(path) + "/txt_logsrebuffers"
arq.close()

executions = ["2", "3", "6"]

#Limiar minimo do buffer
BMin = 0.5
avaliationTime = 720

#Lista todas as execucoes
for execution in executions:
    #Recuperar todos os throughputs relacionados a execucao
    cursor.execute ('SELECT * FROM dash_execution WHERE id = %d' %int(execution))
    ex = cursor.fetchone()
    
    inicialTimeSession = datetime.strptime(ex[1], '%Y-%m-%dT%H:%M:%S.%fZ')

    #Recuperar todos os niveis de buffer relacionados a execucao
    cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(ex[0]))
    buffers = cursor.fetchall()
        
    #calcular rebufferizacoes
    sum_video_times = 0.0
    rebuffer_video_count = 0
    rebuffer_video_flag = True
    durations_video_list = []
    durations_video = []
    session_time1 = datetime.strptime(buffers[0][1], '%Y-%m-%dT%H:%M:%S.%fZ')
    session_time2 = datetime.strptime(buffers[len(buffers) - 1][1], '%Y-%m-%dT%H:%M:%S.%fZ')
    session_time = session_time2 - session_time1
    session_time = session_time.total_seconds()
            
    #Criar o arquivo txt para gravar os tempos de inicio, fim e duracao das rebufferizacoes
    arqLogsRebufferTxt = open(path_logsrebuffers_txt + "/log_rebuffers_exec"+str(ex[0])+".txt" , 'w')
        
    if ex[4]=="video":
        bufferlevel_video_last = int(buffers[0][2])
   
    if ex[4]=="video":
        
        for i in range(len(buffers)):
            bufferlevelvideo = float(buffers[i][2])
            time = datetime.strptime(buffers[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
            time_current =  time - inicialTimeSession                
            time_current =  time_current. total_seconds()
            if bufferlevelvideo <= BMin and bufferlevelvideo < bufferlevel_video_last: 
                if rebuffer_video_flag == True:
                    time1 = time
                    deltaTime1 =  time1 - inicialTimeSession
                    deltaTime1 = deltaTime1.total_seconds()
                    rebuffer_video_flag = False
            elif bufferlevelvideo > BMin and bufferlevelvideo > bufferlevel_video_last:
                if rebuffer_video_flag == False:
                    time2 = time
                    deltaTime2 =  time2 - inicialTimeSession
                    deltaTime2 = deltaTime2.total_seconds()
                    rebuffer_video_flag = True
                    
                    deltaTime = time2 - time1
                    deltaTime = deltaTime.total_seconds()
                                        
                    if time_current <= avaliationTime and time_current >= 60:
                        rebuffer_video_count += 1
                        durations_video = [rebuffer_video_count, deltaTime]
                        arqLogsRebufferTxt.write(str(rebuffer_video_count) +" "+ str(deltaTime)+ "\n")   
                        durations_video_list.append(durations_video)
                        
                        sum_video_times += deltaTime
                        
                        print "Paradas "+str(rebuffer_video_count) +" "+ str(deltaTime)
                        print "Soma dos Tempos"+str(sum_video_times)
                        
            bufferlevel_video_last = bufferlevelvideo
            descontin_tx = float(sum_video_times)/float(avaliationTime - 60)
               
        arqLogsRebufferTxt.close()

        #Media das duracoes das rebufferizacoes de video      
        if(len(durations_video_list) != 0):
            average_duration_rebuffer_video = float(sum_video_times)/float(rebuffer_video_count)
        else:
            average_duration_rebuffer_video = 0

        
        print "Qtde de paradas: %d"%rebuffer_video_count
        print "Descontinuidade: %f"%descontin_tx
        print "Duracao Total das paradas: %f"%sum_video_times
        print "Duracao Media das paradas: %f"%average_duration_rebuffer_video


