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
path_logswitchs_txt = str(path) + "/txt_logspopularity"
path_logsrebuffers_txt = str(path) + "/txt_logsrebuffers"
arq.close()

#Limiar minimo do buffer
BMin = 0.5
avaliationTime = 720.0
#Recuperar todos os executions
cursor.execute ('SELECT * FROM dash_execution')
executions = cursor.fetchall()

#Lista todas as execucoes
for execution in executions:
    
     # Verifica se a execucao eh de video
     # Se for, lista tanto os throughputs, quanto os niveis de buffer
     
     if execution[4] == "video":
        id_execution = execution[0]
        #Pega a metrica FR
        print "------>ExecutionId: %d"%id_execution 
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
        bitrate_last = (int(throughs1[0][3]) + 100) #kbps
        
        #Contar qtde de trocas e a ampplitude das trocas
        for through in throughs1:
            timeThrough = datetime.strptime(through[1], '%Y-%m-%dT%H:%M:%S.%fZ')
            deltaTimeThrough =  timeThrough - inicialTimeSession
            deltaTimeThrough = deltaTimeThrough.total_seconds()
            if deltaTimeThrough <= avaliationTime and deltaTimeThrough >= 60:
                bitrate_parameter = (int(through[3]) + 100)
                bitrates_list.append(bitrate_parameter)
            
                if bitrate_parameter != bitrate_last: 
                    switch_count += 1
                    amplitudes = [bitrate_last, bitrate_parameter, abs(bitrate_last - bitrate_parameter)]
                    amplitudes_list.append(amplitudes)
                
                bitrate_last = bitrate_parameter

        #Pegar a popularidade de cada taxa
        dict_bitrates = dict((i,float(bitrates_list.count(i))/float(len(bitrates_list))*100) for i in bitrates_list)
        dict_bitrates_sorted = sorted(dict_bitrates.items(), key=itemgetter(0))
        
        #frequencia de troca
        tx_switch_freq = switch_count/(avaliationTime - 60)
        #Media das amplitudes entre as representacoes das trocas
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

