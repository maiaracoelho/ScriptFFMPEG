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
path_logswitchs_txt = str(path) + "/txt_logspopularity"
path_logsrebuffers_txt = str(path) + "/txt_logsrebuffers"
arq.close()

#Limiar minimo do buffer
BMin = 0.5
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
        cursor.execute ('SELECT id, time, quality, bandwidth FROM dash_throughseg WHERE fk_execution = %d' %int(id_execution))
        throughs1 = cursor.fetchall()
        inicialTimeSession = datetime.strptime(throughs1[0][1], '%Y-%m-%dT%H:%M:%S.%fZ')

        #Recuperar todos os niveis de buffer relacionados a execucao
        cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(id_execution))
        buffersVideo = cursor.fetchall()
        
        switch_count = 0
        bitrates_list=[]
        amplitudes = []
        amplitudes_list = []
        dict_bitrates={}
        bitrate_last = (int(throughs1[0][3]) + 100) * 1000

        for through in throughs1:
            bitrate_parameter = (int(through[3]) + 100) * 1000
            bitrates_list.append(bitrate_parameter)
            
            if bitrate_parameter != bitrate_last: 
                switch_count += 1
                amplitudes = [bitrate_last, bitrate_parameter, abs(bitrate_last - bitrate_parameter)]
                amplitudes_list.append(amplitudes)
                
            bitrate_last = bitrate_parameter

        #Pegar a popularidade de cada taxa
        dict_bitrates = dict((i,float(bitrates_list.count(i))/float(len(bitrates_list))*100) for i in bitrates_list)
        dict_bitrates_sorted = sorted(dict_bitrates.items(), key=itemgetter(0))
        
        #Taxa de frequencia, tempo total do video eh de 868,8 segundos
        tx_switch_freq = switch_count/868.8
        #Media das amplitudes das entre as representacoes das trocas
        sum_amplitudes_video = 0
        for amplitude in amplitudes_list:
            sum_amplitudes_video += amplitude[2]
        
        average_switch_amplitude_video = sum_amplitudes_video/len(amplitudes_list)

        print dict_bitrates_sorted
        print "Switchs: %d"%switch_count 
        print "SwitchFrequency: %f"%tx_switch_freq
        print "SwitchAmplitudesAverage: %f"%average_switch_amplitude_video
        
        #Criar o arquivo txt para gravar os tempo em segundos e a variacao de largura 
        with open(path_logswitchs_txt + "/" + "log_poplayers_exec"+str(id_execution)+".txt", 'wb') as arqLogsSwTxt:
            w = csv.writer(arqLogsSwTxt, delimiter=' ')
            w.writerows(dict_bitrates_sorted)
        arqLogsSwTxt.close()
        
        rebuffer_video_count = 0
        rebuffervideo_flag = True
        bufferlevelvideo_last = int(buffersVideo[0][2])
        durationsvideo_list = []
        durationsvideo = []
        
        #Criar o arquivo txt para gravar os tempos de inicio, fim e duracao das rebufferizacoes
        arqLogsRebufferTxt = open(path_logsrebuffers_txt + "/log_rebuffers_exec"+str(id_execution)+".txt" , 'w')
        
        for i in range(len(buffersVideo)):
            bufferlevelvideo = float(buffersVideo[i][2])
            time = datetime.strptime(buffersVideo[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
                             
            if bufferlevelvideo < BMin and bufferlevelvideo < bufferlevelvideo_last: 
                if rebuffervideo_flag == True:
                    time1 = time
                    deltaTime1 =  time1 - inicialTimeSession
                    deltaTime1 = deltaTime1.total_seconds()
                    rebuffervideo_flag = False
            elif bufferlevelvideo > bufferlevelvideo_last:
                if rebuffervideo_flag == False:
                    time2 = time
                    deltaTime2 =  time2 - inicialTimeSession
                    deltaTime2 = deltaTime2.total_seconds()
                    
                    rebuffer_video_count += 1
                    rebuffervideo_flag = True
                    
                    deltaTime = time2 - time1
                    deltaTime = deltaTime.total_seconds()
                    
                    if deltaTime <= avaliationTime:
                        durationsvideo = [deltaTime1, deltaTime2, deltaTime]
                        arqLogsRebufferTxt.write(str(deltaTime1) + " " + str(deltaTime) + "\n")   
                        arqLogsRebufferTxt.write(str(deltaTime2) + " " + str(deltaTime) + "\n")                      
                        durationsvideo_list.append(durationsvideo)
            
            bufferlevelvideo_last = bufferlevelvideo  
        
        arqLogsRebufferTxt.close()
        

        tx_bufferVideo_freq = len(durationsvideo_list)/float(avaliationTime)
        #Media das duracoes das rebufferizacoes de video
        duration_sum_video = 0
        for duration in durationsvideo_list:
            duration_sum_video += duration[2]        
        
        if(len(durationsvideo_list) != 0):
            average_duration_rebuffer_video = duration_sum_video/len(durationsvideo_list)
        else:
            average_duration_rebuffer_video = 0

        
        print "Rebufferizacoes Video: %d"%rebuffer_video_count
        print "RebufferVideoFrequency: %f"%tx_bufferVideo_freq
        print "RebufferAudioAverageDuration: %f"%average_duration_rebuffer_video


