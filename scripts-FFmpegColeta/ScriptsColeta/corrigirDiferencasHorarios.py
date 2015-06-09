'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import MySQLdb
import string
from datetime import datetime, timedelta, tzinfo
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


#Recuperar todos os experimento que possuem o atributo algorithm = RAR ou RMR ou ainda MILLER
cursor.execute ('SELECT * FROM dash_execution WHERE id = 31')
execution = cursor.fetchone()


timeExecution = datetime.strptime(execution[1], '%Y-%m-%dT%H:%M:%S.%fZ')
timeExecution = timeExecution + timedelta(hours=14) 
timeExecution = timeExecution + timedelta(minutes=34) 
timeExecution = timeExecution + timedelta(seconds=13) 
timeExecution = timeExecution.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print "ExecutionId: %d - time %s - new time: %s"%(execution[0], execution[1], timeExecution)
cursor.execute ('UPDATE dash_execution SET execution_time = "%s" WHERE id = %d' %(str(timeExecution), int(execution[0])))
connection.commit()

#Recuperar todos os throughputs relacionados ao primeiro experimento
cursor.execute ('SELECT * FROM dash_throughseg WHERE fk_execution = %d' %int(execution[0]))
throughs = cursor.fetchall()
for through in throughs:
    timeThrough = datetime.strptime(through[2], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeStartThrough = datetime.strptime(through[3], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeResponseThrough = datetime.strptime(through[4], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeFinishThrough = datetime.strptime(through[5], '%Y-%m-%dT%H:%M:%S.%fZ')

    timeThrough = timeThrough + timedelta(hours=14) 
    timeThrough = timeThrough + timedelta(minutes=34) 
    timeThrough = timeThrough + timedelta(seconds=13) 
    
    timeStartThrough = timeStartThrough + timedelta(hours=14) 
    timeStartThrough = timeStartThrough + timedelta(minutes=34) 
    timeStartThrough = timeStartThrough + timedelta(seconds=13) 
    
    timeResponseThrough = timeResponseThrough + timedelta(hours=14) 
    timeResponseThrough = timeResponseThrough + timedelta(minutes=34) 
    timeResponseThrough = timeResponseThrough + timedelta(seconds=13) 
    
    timeFinishThrough = timeFinishThrough + timedelta(hours=14) 
    timeFinishThrough = timeFinishThrough + timedelta(minutes=34) 
    timeFinishThrough = timeFinishThrough + timedelta(seconds=13) 
    
    timeThrough = timeThrough.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timeStartThrough = timeStartThrough.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timeResponseThrough = timeResponseThrough.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timeFinishThrough = timeFinishThrough.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    cursor.execute ('UPDATE dash_throughseg SET time = "%s", start_time = "%s", response_time = "%s", finish_time = "%s" WHERE id = %d' %(str(timeThrough), str(timeStartThrough), str(timeResponseThrough), str(timeFinishThrough), int(through[0])))
    connection.commit()
    
#Recuperar todos os throughputs relacionados ao primeiro experimento
cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(execution[0]))
buffers = cursor.fetchall()
for buffer in buffers:
    timeBuffer = datetime.strptime(buffer[1], '%Y-%m-%dT%H:%M:%S.%fZ')
    timeBuffer = timeBuffer + timedelta(hours=14) 
    timeBuffer = timeBuffer + timedelta(minutes=34) 
    timeBuffer = timeBuffer + timedelta(seconds=13) 
    timeBuffer = timeBuffer.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    cursor.execute ('UPDATE dash_bufferlevel SET time = "%s" WHERE id = %d' %(str(timeBuffer), int(buffer[0])))
    connection.commit()

'''
#Recuperar todos os throughputs relacionados ao primeiro experimento
cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(idExecucao))
buffers1 = cursor.fetchall()
'''
