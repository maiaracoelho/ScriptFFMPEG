'''
Created on 13/07/2015

@author: Maiara
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

experiment = 1  
executions = []

for execution in executions:
    print execution
    cursor.execute ('INSERT INTO dash_experiments (num_experiment, fk_execution) VALUES (%d,%d)' %(int(experiment),int(execution)))
    connection.commit()

print "Gravou"