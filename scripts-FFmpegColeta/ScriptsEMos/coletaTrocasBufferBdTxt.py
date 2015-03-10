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
path, logbw,  idExecucao = linha.split()
path_logswitchs_txt = str(path) + "/txt_logspopularity"
arq.close()

#Limiar minimo do buffer
BMin = 10
#Recuperar todos os executions
cursor.execute ('SELECT * FROM dash_execution')
executions = cursor.fetchall()

#Lista todas as execucoes
for execution in executions:
    #Verifica se eh audio
     if execution[4] == "audio":
        id_execution = execution[0]
        print "----->ExecutionId: %d"%id_execution 
       
        #Recuperar todos os buffers relacionados a execucao
        cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(id_execution))
        buffersAudio = cursor.fetchall()
        
        rebuffer_audio_count = 0
        rebufferaudio_flag = True
        bufferlevel_last = int(buffersAudio[0][2])
        durations_list = []
        durationsaudio = []
        
        #Lista todos os buffers de audio para verificar as ocorrencias de rebufferizacao
        for i in range(len(buffersAudio)):
            bufferlevel = float(buffersAudio[i][2])
            time = datetime.strptime(buffersAudio[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
            
            # Verifica se o nivel do buffer esta abaixo do limiar inferior
            # Verifica tb se o nivel do buffer atual eh menor do que o passado
            # Se for, verifica se o flag esta em verdadeiro
            # Se estiver que dizer que o buffer esta esvaziando e acontecera a rebufferizacao
            # Pega o tempo inicial time1
            
            if bufferlevel < BMin and bufferlevel < bufferlevel_last: 
                if(rebufferaudio_flag == True):
                    time1 = time
                    rebufferaudio_flag = False
            # Verifica se o nivel atual do buffer eh maior do que o passado 
            # Se for, verifica se a flag esta em false
            # Se estiver eh sinal de que a rebufferizacao esta ocorrendo
            # Pega o tempo final time2
           
            elif bufferlevel > bufferlevel_last:
                if(rebufferaudio_flag == False):
                    time2 = time
                    rebuffer_audio_count += 1
                    rebufferaudio_flag = True
                    deltaTime = time2 - time1
                    deltaTime = deltaTime.total_seconds()
                    durationsaudio = [time1.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), time2.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), deltaTime]
                    durations_list.append(durationsaudio)
                    
            
            bufferlevel_last = bufferlevel  
        
        tx_bufferAudio_freq = len(durations_list)/868.8
        print "Rebufferizacoes Audio: %d"%rebuffer_audio_count
        print "RebufferAudioFrequency: %f"%tx_bufferAudio_freq
        print durations_list
    
     # Verifica se a execucao eh de video
     # Se for, lista tanto os throughputs, quanto os niveis de buffer
     
     elif execution[4] == "video":
        id_execution = execution[0]
        mpd_peaces = execution[3].split("/")
        #Pega a metrica FR
        fr_parameter = mpd_peaces[5]
        print "------>ExecutionId: %d"%id_execution 
        print "FRparameter: %s"%fr_parameter # Pegar FR
        #Recuperar todos os throughputs relacionados a execucao
        cursor.execute ('SELECT id, time, quality, bandwidth FROM dash_throughseg WHERE fk_execution = %d' %int(id_execution))
        throughs1 = cursor.fetchall()

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
        print dict_bitrates_sorted
        print amplitudes_list
        print "Switchs: %d"%switch_count 
        print "SwitchFrequency: %f"%tx_switch_freq

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
        
        for i in range(len(buffersVideo)):
            bufferlevelvideo = float(buffersVideo[i][2])
            time = datetime.strptime(buffersVideo[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
                             
            if bufferlevelvideo < BMin and bufferlevelvideo < bufferlevelvideo_last: 
                if rebuffervideo_flag == True:
                    time1 = time
                    rebuffervideo_flag = False
            elif bufferlevelvideo > bufferlevelvideo_last:
                if rebuffervideo_flag == False:
                    time2 = time
                    rebuffer_video_count += 1
                    rebuffervideo_flag = True
                    deltaTime = time2 - time1
                    deltaTime = deltaTime.total_seconds()
                    durationsvideo = [time1.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), time2.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), deltaTime]
                    durationsvideo_list.append(durationsvideo)
            
            bufferlevelvideo_last = bufferlevelvideo  
        
        tx_bufferVideo_freq = len(durationsvideo_list)/868.8
        print "Rebufferizacoes Video: %d"%rebuffer_video_count
        print "RebufferVideoFrequency: %f"%tx_bufferVideo_freq
        print durationsvideo_list
