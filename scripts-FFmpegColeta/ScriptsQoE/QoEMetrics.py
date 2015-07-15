#!/usr/bin/env python

import time
import os
import sys
import string
import MySQLdb

def conectaBanco():
 
    HOST = "localhost"
    USER = "root"
    PASSWD = "mysql"
    BANCO = "dash_db"
 
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
#estivessem reproduzindo vídeo, ao mesmo tempo
def definirTempoIFAvaliacao(conecta):
 
    vetor = str(raw_input("\nDigite o(s) Id(s) da(s) execucao(oes) separados por espaco: "))
    vetor = map(int, vetor.split())
    
    cursor = conecta.cursor()
    
    sql="SELECT time, start_time, finish_time FROM  dash_throughseg WHERE fk_execution='"+vetor[0]+"'"
    resultados = 0
    
    try:
         cursor.execute(sql)
         resultado = cursor.fetchall()
         for dados in resultado:
              time = datetime.strptime(dados[0], '%Y-%m-%dT%H:%M:%S.%fZ') 
              start_time = datetime.strptime(dados[1], '%Y-%m-%dT%H:%M:%S.%fZ') 
              finish_time = datetime.strptime(dados[2], '%Y-%m-%dT%H:%M:%S.%fZ') 
              resultados= int(resultados)
              print"\n----------------------------\n"
              print " %s\n Time: %s\n StartTime: %s\n FinishTime: %s"%(time, start_time, finish_time)
              conecta.commit()
              
              #fazer o start_time ser o maior e o finish_time ser o menor tempo
              maior_time_inicial = start_time
              menor_time_final = finish_time

              resultados = resultados + 1
              
    except MySQLdb.Error, e:
          print "Erro: " + sql
          print e
            
    
    for i in range(1,len(vetor)):
        sql="SELECT time, start_time, finish_time FROM dash_throughseg WHERE fk_execution='"+vetor[i]+"'"
        resultados = 0
 
        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for dados in resultado:
                ide = dados[0]
                nome = dados[1]
                ndereco = dados[2]
                mail = dados[3]
                telefone = dados[4]
                resultados= int(resultados)
                resultados = resultados + 1
                print"\n----------------------------\n"
                print " ID: %s\n Nome: %s\n Endereco: %s\n Email: %s\n Telefone: %s"%(ide, nome, endereco, email, telefone)
                conecta.commit()
 
        except MySQLdb.Error, e:
            print "Erro: " + sql
            print e
 
    print "\n\nForam encontrados %d resultados"%resultados
    conecta.close()
    menu = raw_input()
    os.system("clear")
    menu()
    
def menu():
 
    os.system("clear");
    print "==================================="
    print "======= QoE Metrics ========"
    print "==================================="
    opcao = raw_input("Escolha opcao desejada\n\n[1] - Coletar Trocas e Amplitudes\n[2] - Coletar Stalls e Duracoes de Stalls\n[3] - Coletar Taxa media e Justica\n[4] - Coletar Instabilidade\n[5] - Gerar Graficos Gerais\n[6] - Sair")
 
    try:
        opcao = int(opcao)
        if opcao<1 or opcao>6:
            os.system("clear");
            print "OPCAO INVALIDA: Verifique o valor digitado"
            time.sleep(2)
            menu()
    except:
        os.system("clear");
        print "OPCAO INVALIDA: Verifique o valor digitado"
        time.sleep(2)
        menu()
 
    if opcao == 1:
        conecta = conectaBanco()
        prepararListaSegmentos(conecta)
        coletarTrocasAmplitudes(conecta)
 
    elif opcao == 2:
        conecta = conectaBanco()
        coletarSrtallsDuracoes(conecta)
 
    elif opcao == 3:
        conecta = conectaBanco()
        coletarTaxaJustica(conecta)
 
    elif opcao == 4:
        conecta = conectaBanco()
        coletarInst(conecta)
 
    elif opcao == 5:
        conecta = conectaBanco()
        gerarGraficos(conecta)
 
    elif opcao == 6:
        sys.exit()

if __name__=='__main__':
    menu()