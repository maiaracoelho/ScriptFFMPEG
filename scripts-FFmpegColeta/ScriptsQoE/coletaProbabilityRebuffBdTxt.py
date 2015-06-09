'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import MySQLdb
import string
from datetime import datetime, timedelta
import math
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
path, idExecucao1, idExecucao2, idExecucao3, alg = linha.split()
path_logsprob_txt = str(path) + "/txt_logsprobability"
arq.close()

#Limiar minimo do buffer
BMin = 10
Breb = 0.5
avaliationTime = 720

#Recuperar todos os executions
cursor.execute ('SELECT * FROM dash_execution where id = %d' % int(idExecucao1))
execution = cursor.fetchone()

# Verifica se a execucao eh de video
# Se for, lista tanto os throughputs, quanto os niveis de buffer
     
#if execution[4] == "video":
#        id_execution = execution[0]
#        mpd_peaces = execution[3].split("/")
#inicialTimeSession = datetime.strptime(execution[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        #Pega a metrica FR
#        fr_parameter = mpd_peaces[5]
print "------>ExecutionId: %s"%str(idExecucao1)
#        print "FRparameter: %s"%fr_parameter # Pegar FR

#Recuperar todos os niveis de buffer relacionados a execucao
cursor.execute ('SELECT * FROM dash_bufferlevel WHERE fk_execution = %d' %int(idExecucao1))
buffersVideo = cursor.fetchall()

inicialTimeSession = datetime.strptime(buffersVideo[0][1], '%Y-%m-%dT%H:%M:%S.%fZ')
          
listaBuffer = buffersVideo[::-1]


listaProbabilityTxt = []
probability = []
probabilidade_sum = 0
countReb_sum = 0
for i in  range(len(listaBuffer)):
    bufferlevelvideo = float(listaBuffer[i][2])
    time = datetime.strptime(listaBuffer[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
    time1 = time
    deltaTime1 =  time1 - inicialTimeSession   
    deltaTime2 = deltaTime1 + timedelta(seconds=-15) 
    deltaTime1 = deltaTime1.total_seconds()
    deltaTime2 = deltaTime2.total_seconds()
            
    countGreater = 0
    countSmaller = 0
    countReb = 0
            
    if deltaTime2 >= 0 and deltaTime1 >= 15 and deltaTime1 <= avaliationTime:
        internalIndice = i
        print "delta2: "+str(deltaTime2) +" delta1: "+ str(deltaTime1)
                
        while (internalIndice < len(listaBuffer)):
            timeCurrentInternal = (datetime.strptime(listaBuffer[internalIndice][1], '%Y-%m-%dT%H:%M:%S.%fZ')- inicialTimeSession).total_seconds() 
            if timeCurrentInternal >= deltaTime2 and timeCurrentInternal <= deltaTime1:
                #print "Level: "+ listaBuffer[internalIndice][2] + " Time: " +str(timeCurrentInternal)

                if float(listaBuffer[internalIndice][2]) > float(BMin):
                    countGreater += 1
                else:
                    countSmaller += 1
                    if float(listaBuffer[internalIndice][2]) <= float(Breb):
                        countReb += 1
                        
            internalIndice += 1
        
        print countGreater, countSmaller, countReb
        #probabilidade = float(countSmaller)/(float(countGreater) + float(countSmaller))
        probabilidade = float(countSmaller)/(float(countGreater) + float(countSmaller))
        probabilidade_sum += probabilidade
        countReb_sum += countReb
        print probabilidade
        probability = [deltaTime1, probabilidade]
        listaProbabilityTxt.append(probability)

averageProb = probabilidade_sum/len(listaProbabilityTxt)
print "Media de Probabilidade: " + str(averageProb)
print "Numero de RBuf: " + str(countReb_sum)
        
#Criar o arquivo txt para gravar os tempos de inicio, fim e duracao das rebufferizacoes
arqLogsProbabilityTxt = open(path_logsprob_txt + "/log_probability_exec"+str(idExecucao1)+".txt" , 'w')
for prob in  reversed(listaProbabilityTxt):
    #print prob
    arqLogsProbabilityTxt.write(str(prob[0]) + " " + str(prob[1]*100) + "\n") 
    
arqLogsProbabilityTxt.close()  
        
            
                

