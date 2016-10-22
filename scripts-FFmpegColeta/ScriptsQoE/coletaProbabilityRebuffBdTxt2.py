'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python

import time
from os import system, remove
import sys
import string
import MySQLdb
import math
from datetime import datetime, timedelta
from operator import itemgetter
import Gnuplot, Gnuplot.funcutils

def conectaBanco():
    HOST = "localhost"
    USER = "root"
    PASSWD = "mysql"
    BANCO = "dash_db2"
 
    try:
        conecta = MySQLdb.connect(HOST, USER, PASSWD)
        conecta.select_db(BANCO)
 
    except MySQLdb.Error, e:
        print "Erro: Banco nao encontrado",e
        menu = raw_input()
        os.system("clear")
        menu()
    
    return conecta

#alinha as execucoes para que as sessoes sejam avaliadas no periodo em que todas 
#estivessem reproduzindo video, ao mesmo tempo
def definirTempoInicialExecution(conecta, vetor):
    
    cursor = conecta.cursor()
    sql="SELECT * FROM  dash_execution WHERE id=%d"%int(vetor[0])
    try:
         cursor.execute(sql)
         execution = cursor.fetchone()
         
         start_time = datetime.strptime(execution[1], '%Y-%m-%dT%H:%M:%S.%fZ') 
         #print"\n----------------------------\n"
         #print " ID: %s\n StartTime: %s"%(int(vetor[0]), start_time)
              
         #fazer o start_time ser o maior e o finish_time ser o menor tempo
         maior_time_inicial = start_time
    
    except MySQLdb.Error, e:
          print "Erro: " + sql
          print e
            
    for i in range(1,len(vetor)):
        sql="SELECT * FROM dash_execution WHERE id=%d"%int(vetor[i])
        try:
            cursor.execute(sql)
            execution = cursor.fetchone()
              
            start_time = datetime.strptime(execution[1], '%Y-%m-%dT%H:%M:%S.%fZ') 
            #print"\n----------------------------\n"
            #print " ID: %s\n StartTime: %s"%(int(vetor[i]), start_time)
              
            #fazer o start_time ser o maior e o finish_time ser o menor tempo se forem respectivamente, maior e menor
            #que maior_time_inicial e menor_time_final
            if start_time > maior_time_inicial:
                maior_time_inicial = start_time
            
        except MySQLdb.Error, e:
            print "Erro: Banco nao encontrado",e
            menu = raw_input()
            os.system("clear")
            menu()
            
    return maior_time_inicial
    
def definirTempoFinalExecution(conecta, executions):
 
    cursor = conecta.cursor()
    sql="SELECT * FROM  dash_execution WHERE id=%d"%int(executions[0])
    try:
         cursor.execute(sql)
         execution = cursor.fetchone()
              
         finish_time = datetime.strptime(execution[2], '%Y-%m-%dT%H:%M:%S.%fZ') 
         #print"\n----------------------------\n"
         #print " ID: %s\n FinishTime: %s"%(int(executions[0]), finish_time)
              
         #fazer o start_time ser o maior e o finish_time ser o menor tempo
         menor_time_final = finish_time
    
    except MySQLdb.Error, e:
          print "Erro: " + sql
          print e
            
    
    for i in range(1,len(executions)):
        sql="SELECT * FROM  dash_execution WHERE id=%d"%int(executions[0])
        try:
            cursor.execute(sql)
            execution = cursor.fetchone()
              
            finish_time = datetime.strptime(execution[2], '%Y-%m-%dT%H:%M:%S.%fZ') 
            #print"\n----------------------------\n"
            #print " ID: %s\n FinishTime: %s"%(int(executions[i]), finish_time)
              
            #fazer o start_time ser o maior e o finish_time ser o menor tempo se forem respectivamente, maior e menor
            #que maior_time_inicial e menor_time_final
            if finish_time < menor_time_final:
                menor_time_final = finish_time
              
        except MySQLdb.Error, e:
            print "Erro: Banco nao encontrado",e
            menu = raw_input()
            os.system("clear")
            menu()
            
    return menor_time_final

#programa principal
conecta = conectaBanco()

executions = str(raw_input("\nDigite o(s) Id(s) da(s) execucao(oes) separados por espaco: "))
executions = map(int, executions.split())
#path = str(raw_input("\nDigite o caminho para salvar o txt: "))
#Corte para tempo de sessao total
inicial_time = definirTempoInicialExecution(conecta, executions)
final_time = definirTempoFinalExecution(conecta, executions)
timeSession =  final_time - inicial_time
timeSession = timeSession.total_seconds()
print "delta: %s"%timeSession

path_logsprob_txt = "/home/dash/Dropbox/Pesquisas_Mestrado/experimentos/experimentos-07-07-15/txt_logsprobability"
path_graphs_prob = "/home/dash/Dropbox/Pesquisas_Mestrado/experimentos/experimentos-07-07-15/graphs_probability"

#Limiar minimo do buffer
BMin = 10
Breb = 0.5
arqLogsProbabilityTxtList = []

cursor = conecta.cursor()

for i in range(0,len(executions)):
        
        #Recuperar todos os niveis de buffer relacionados a execucao
        sql="SELECT * FROM dash_bufferlevel WHERE fk_execution = %d"%int(executions[i])
        try:
            cursor.execute(sql)
            buffersVideo = cursor.fetchall()
              
        except MySQLdb.Error, e:
            print "Erro: Banco nao encontrado",e
            menu = raw_input()
            os.system("clear")
            menu()
        
        listaBuffer = buffersVideo[::-1]
        listaProbabilityTxt = []
        probability = []
        probabilidade_sum = 0.0
        countReb_sum = 0
        
        #Criar o arquivo txt para gravar os tempos de inicio, fim e duracao das rebufferizacoes
        arqLogsProbabilityTxt = open(path_logsprob_txt + "/log_probability_exec"+str(executions[i])+".txt" , 'w')
        arqLogsProbabilityTxtList.append(path_logsprob_txt + "/log_probability_exec"+str(executions[i])+".txt")
        
        for i in  range(len(listaBuffer)):
            bufferlevelvideo = float(listaBuffer[i][2])
            time = datetime.strptime(listaBuffer[i][1], '%Y-%m-%dT%H:%M:%S.%fZ')
            time1 = time
            deltaTime1 =  time1 - inicial_time   
            deltaTime2 = deltaTime1 + timedelta(seconds=-15) 
            deltaTime1 = deltaTime1.total_seconds()
            deltaTime2 = deltaTime2.total_seconds()
            
            countGreater = 0
            countSmaller = 0
            countReb = 0
    
            if time >= inicial_time and time <= final_time and deltaTime2 >= 0 and deltaTime1 >= 15:
                internalIndice = i
                print "delta2: "+str(deltaTime2) +" delta1: "+ str(deltaTime1)
                
                while (internalIndice < len(listaBuffer)):
                    timeCurrentInternal = (datetime.strptime(listaBuffer[internalIndice][1], '%Y-%m-%dT%H:%M:%S.%fZ')- inicial_time).total_seconds() 
                    if timeCurrentInternal >= deltaTime2 and timeCurrentInternal <= deltaTime1:
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
                #print probabilidade
                probability = [deltaTime1, probabilidade]
                listaProbabilityTxt.append(probability)
            
       
        print listaProbabilityTxt       
        
        for prob in reversed(listaProbabilityTxt):
            #print prob
            arqLogsProbabilityTxt.write(str(prob[0]) + " " + str(prob[1]*100) + "\n") 
    
        arqLogsProbabilityTxt.close()  
        
        print arqLogsProbabilityTxtList
                

