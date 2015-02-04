'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import MySQLdb
import string
from datetime import datetime, timedelta

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

# Pegar o id do experimento
executionId = input('Entre com o id da Execucao: ')

#Recuperar o experimento do banco
cursor.execute ('SELECT * FROM dash_execution WHERE id = %d' %executionId)
execution1 = cursor.fetchone()
#Recuperar o experimento que possui o time igual ao do expeimento anterior - Isso eh pq video e audio sao separados
cursor.execute ('SELECT * FROM dash_execution WHERE execution_time = "%s" AND id != %d' %(execution1[1], execution1[0]) )
execution2 = cursor.fetchone()

#Recuperar todos os throughputs relacionados ao primeiro experimento
cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %execution1[0])
throughs1 = cursor.fetchall()

#Recuperar todos os throughputs relacionados ao segundo experimento
cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %execution2[0])
throughs2 = cursor.fetchall()

timeInitialThrough1 = datetime.strptime(throughs1[0][3], '%Y-%m-%dT%H:%M:%S.%fZ')

print timeInitialThrough1

for through in throughs1:
    print datetime.strptime(through[3], '%Y-%m-%dT%H:%M:%S.%fZ')-timeInitialThrough1

for through in throughs2:
    print datetime.strptime(through[3], '%Y-%m-%dT%H:%M:%S.%fZ')-timeInitialThrough1


logbw = "/home/dash/Dropbox/Pesquisas_Mestrado/experimentos/experimentos1/dash_logs_bw/logbw_dashdataset_26-01-15/logbw1_rcr_cenario1_gran120_fps7.txt"
arq=open(logbw,"r")
row1 = arq.readline()
rows = arq.readlines()

dataInicial, initialTimeLogBw, Bw  = rows[0].split()
initialTimeLogBw = datetime.strptime(initialTimeLogBw, '%H:%M:%S.%f')
print initialTimeLogBw

for row in rows:
    date, time, bitRate= row.split()
    time = datetime.strptime(time, '%H:%M:%S.%f') - initialTimeLogBw
    print time , bitRate

    

