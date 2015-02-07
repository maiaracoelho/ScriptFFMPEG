'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import MySQLdb
import string
from datetime import datetime, timedelta
import string


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

path_logsbw = str(path) + "/dash_logs_bw"
path_logsbw_txt = str(path) + "/txt_logbw"
path_video_txt = str(path) + "/txt_video"

nameLogs = str(logbw).split("_")
nameLogs = nameLogs[0] + ".txt"
arq.close()

#Recuperar o experimento do banco
cursor.execute ('SELECT * FROM dash_execution WHERE stream = "video"')
exe = cursor.fetchone()

#Recuperar o experimento que possui o time igual ao do expeimento anterior - Isso eh pq video e audio sao separados
cursor.execute ('SELECT * FROM dash_execution WHERE execution_time = "%s" AND id != %d' %(execution1[1], execution1[0]) )
execution2 = cursor.fetchone()


#Recuperar todos os throughputs relacionados ao primeiro experimento
cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %execution1[0])
throughs1 = cursor.fetchall()
print execution1[0]


#Recuperar todos os throughputs relacionados ao segundo experimento
cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %execution2[0])
throughs2 = cursor.fetchall()
print execution2[0]

#Abrir o arquivo de log de variacoes de bw
arqLogsBw=open(path_logsbw + "/" + logbw,"r")
row1 = arqLogsBw.readline()
rows = arqLogsBw.readlines()

#Tratar tempos do arqBw
dataInicial, initialTimeLogBw, Bw  = rows[0].split()
initialTimeTotalLogBw = datetime.strptime(dataInicial + " " +initialTimeLogBw, '%Y-%m-%d %H:%M:%S.%f') 
print initialTimeTotalLogBw

#Criar o arquivo txt para gravar os tempo em segundos e a variacao de largura 
arqLogsBwTxt = open(path_logsbw_txt + "/" + nameLogs , 'w')

for row in rows:
    date, time, bitRate= row.split()
    time = datetime.strptime(date + " " +time, '%Y-%m-%d %H:%M:%S.%f')
    time =  time - initialTimeTotalLogBw
    time =  time.total_seconds()
    bitRate = int(bitRate)/1000
    arqLogsBwTxt.write(str(time) + " " +  str(bitRate) + "\n")   
    print time , str(bitRate)

arqLogsBwTxt.close()
arqLogsBw.close()

#Criar o arquivo txt para gravar os tempos e os bit rates do video e somar com o bitrate do audio
arqLogsBrTxt = open(path_video_txt + "/" + nameLogs , 'w')

#Tratar tempo para o throughput1 
for through in throughs1:
    timeInitialThrough1 = datetime.strptime(through[3], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeInitialThrough1 = timeInitialThrough1 + timedelta(hours=-4)
    if (timeInitialThrough1 > initialTimeTotalLogBw):
        timeInitialThrough1 =  timeInitialThrough1 - initialTimeTotalLogBw
        timeInitialThrough1 =  timeInitialThrough1.total_seconds()
        #Converter de bit/ms para bit/s
        bitrate = int(through[9]) + 100

        arqLogsBrTxt.write(str(timeInitialThrough1) + " " +  str(bitrate) + "\n")   
        print timeInitialThrough1, bitrate
        
arqLogsBrTxt.close()

#Tratar tempo para o throughput2
'''for through in throughs2:
    timeInitialThrough2 = datetime.strptime(through[3], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeInitialThrough2 = timeInitialThrough2 + timedelta(hours=-4)
    if (timeInitialThrough2 > initialTimeLogBw):
        timeInitialThrough2 =  timeInitialThrough2 - initialTimeLogBw
        timeInitialThrough2 =  timeInitialThrough2.total_seconds()
        #Converter de bit/ms para bit/s
        bitrate = int(through[9]) * 1000             
        print timeInitialThrough2, bitrate
'''
        


    

