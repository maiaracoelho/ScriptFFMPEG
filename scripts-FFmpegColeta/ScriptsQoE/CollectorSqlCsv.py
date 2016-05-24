#!/usr/bin/env python

import time
import os
import sys
import string
import MySQLdb
import math
from datetime import datetime, timedelta
from operator import itemgetter

def conectaBanco():
 
    HOST = "localhost"
    USER = "root"
    PASSWD = "mysql"
    BANCO = "dash_db5"
 
    try:
        conecta = MySQLdb.connect(HOST, USER, PASSWD)
        conecta.select_db(BANCO)
 
    except MySQLdb.Error, e:
        print "Erro: Banco nao encontrado",e
        menu = raw_input()
        os.system("clear")
        menu()
    
    return conecta


def definirTempoInicialSegmento(conecta, vetor):
    
    cursor = conecta.cursor()
    sql="SELECT time, start_time, finish_time FROM  dash_throughseg WHERE fk_execution=%d"%int(vetor[0])
    try:
         cursor.execute(sql)
         segmentos = cursor.fetchall()
              
         start_time = datetime.strptime(segmentos[0][1], '%Y-%m-%dT%H:%M:%S.%fZ') 
         #print"\n----------------------------\n"
         #print " ID: %s\n StartTime: %s"%(int(vetor[0]), start_time)
              
         #fazer o start_time ser o maior e o finish_time ser o menor tempo
         maior_time_inicial = start_time
    
    except MySQLdb.Error, e:
          print "Erro: " + sql
          print e
            
    for i in range(1,len(vetor)):
        sql="SELECT time, start_time, finish_time FROM dash_throughseg WHERE fk_execution=%d"%int(vetor[i])
        try:
            cursor.execute(sql)
            segmentos = cursor.fetchall()
              
            start_time = datetime.strptime(segmentos[0][1], '%Y-%m-%dT%H:%M:%S.%fZ') 
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
    
def definirTempoFinalSegmento(conecta, executions):
 
    cursor = conecta.cursor()
    sql="SELECT time, start_time, finish_time FROM  dash_throughseg WHERE fk_execution=%d"%int(executions[0])
    try:
         cursor.execute(sql)
         segmentos = cursor.fetchall()
              
         finish_time = datetime.strptime(segmentos[len(segmentos) - 1][2], '%Y-%m-%dT%H:%M:%S.%fZ') 
         #print"\n----------------------------\n"
         #print " ID: %s\n FinishTime: %s"%(int(executions[0]), finish_time)
              
         #fazer o start_time ser o maior e o finish_time ser o menor tempo
         menor_time_final = finish_time
    
    except MySQLdb.Error, e:
          print "Erro: " + sql
          print e
            
    
    for i in range(1,len(executions)):
        sql="SELECT time, start_time, finish_time FROM dash_throughseg WHERE fk_execution=%d"%int(executions[i])
        try:
            cursor.execute(sql)
            segmentos = cursor.fetchall()
              
            finish_time = datetime.strptime(segmentos[len(segmentos) - 1][2], '%Y-%m-%dT%H:%M:%S.%fZ') 
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

'''Funcao para coletar a qtde de interrupcoes, a duracao media das interrupcoes por execucao e a media entre as execucoes informadas'''        
def coletarPopularity(conecta):
   
    cursor = conecta.cursor()
    
    sql="SELECT dash_throughseg.start_time, dash_throughseg.finish_time, dash_throughseg.size_seg, dash_throughseg.duration, dash_throughseg.bitrate, dash_throughseg.throughseg, dash_execution.algorithm, dash_execution.url_mpd, dash_execution.scenario
FROM dash_throughseg
INNER JOIN dash_execution ON dash_throughseg.fk_execution = dash_execution.id
WHERE dash_throughseg.stream =  'video'
    
    inicial_time = definirTempoInicialExecution(conecta, executions)
    final_time = definirTempoFinalExecution(conecta, executions)
    timeSession =  final_time - inicial_time
    timeSession = timeSession.total_seconds()
    print "Tempo da Sessao: %s"%timeSession
    
    for i in range(0,len(executions)):
        

        try:
            cursor.execute(sql2)
            segmentos = cursor.fetchall()
            
        except MySQLdb.Error, e:
            print "Erro: Banco nao encontrado",e
            menu = raw_input()
            os.system("clear")
            menu()
            
        bitrates_list=[]
        dict_bitrates={}
        for seg in segmentos:            
            start_time_seg = datetime.strptime(seg[1], '%Y-%m-%dT%H:%M:%S.%fZ')
            finish_time_seg = datetime.strptime(seg[2], '%Y-%m-%dT%H:%M:%S.%fZ')
            if start_time_seg >= inicial_time and finish_time_seg <= final_time:
                
                bitrate_parameter = float(seg[6]) + 100
                bitrates_list.append(bitrate_parameter)

       #Pegar a popularidade de cada taxa
        dict_bitrates = dict((i,float(bitrates_list.count(i))/float(len(bitrates_list))*100) for i in bitrates_list)
        dict_bitrates_sorted = sorted(dict_bitrates.items(), key=itemgetter(0))
        
        print dict_bitrates_sorted 
                    

    print "==================================="
   
    

if __name__=='__main__':
    
    os.system("clear");
    print "Aguarde enquanto o coletor transforma de SQL para CSV com os seguintes atributos:download_time_seg, size_seg, duration_seg, throughput_seg, algorithm, scenario?, bitrate_seg"
    print "==================================="
 
    conecta = conectaBanco()
    coletarTrocasAmplitudes(conecta)
