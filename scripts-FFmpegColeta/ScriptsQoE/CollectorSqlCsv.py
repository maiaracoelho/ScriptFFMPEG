#!/usr/bin/env python

import time
import os
import sys
import string
import MySQLdb
import math
from datetime import datetime, timedelta
from operator import itemgetter
import arff
import json

#easy_install liac-arff
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

'''Funcao para coletar'''
def coletar(conecta):

    cursor = conecta.cursor()

    sql1="SELECT dash_throughseg.start_time, dash_throughseg.finish_time, dash_throughseg.size_seg, dash_throughseg.duration, dash_throughseg.bitrate, dash_throughseg.throughseg, dash_execution.algorithm, dash_execution.scenario, dash_execution.stream FROM dash_throughseg INNER JOIN dash_execution ON dash_throughseg.fk_execution = dash_execution.id WHERE dash_throughseg.stream =  'video'"

    try:
        cursor.execute(sql1)
        segmentos = cursor.fetchall()

    except MySQLdb.Error, e:
        print "Erro: Banco nao encontrado",e
        
    
    cont=0
    data = []
    data_list = []
    for seg in segmentos:
        start_time_seg = datetime.strptime(seg[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        finish_time_seg = datetime.strptime(seg[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        download_time =  finish_time_seg - start_time_seg
        download_time_seg = download_time.total_seconds()
        size_seg = seg[2]
        duration_seg = seg[3]
        bitrate_seg = seg[4]
        throughput_seg = seg[5]
        algorithm = seg[6]
        scenario = seg[7]
        #stream = seg[8]
        cont=cont+1
        
        data = [download_time_seg,size_seg,duration_seg,bitrate_seg,str(algorithm),scenario]
        data_list.append(data)
        
        print "Cont: %s"%cont
        #print "DownloadTime: %s"%download_time_seg
        #print "Segment Size: %s"%size_seg
        #print "Segment Duration: %s"%duration_seg
        #print "Segment Throughput: %s"%throughput_seg
        ##print "Algorithm: %s"%algorithm
        #print "Scenario: %s"%scenario
        #print "Bitrate: %s"%bitrate_seg

        print "==================================="
    
    arff.dump(open('/home/dash/Dropbox/Pesquisa_Doctor/AMMD Pessoal/base.arff', 'w'), data_list, relation="segments", names=['download_time_seg', 'size_seg', 'duration_seg', 'bitrate_seg', 'algorithm', 'scenario'])     

if __name__=='__main__':

    os.system("clear");
    print "Aguarde enquanto o coletor transforma de SQL para CSV com os seguintes atributos:download_time_seg, size_seg, duration_seg, throughput_seg, algorithm, scenario, bitrate_seg"
    print "==================================="

    conecta = conectaBanco()
    coletar(conecta)