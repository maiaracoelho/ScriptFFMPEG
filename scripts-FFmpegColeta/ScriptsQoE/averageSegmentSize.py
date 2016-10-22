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

def AverageHighSegmentSize(conecta):

    cursor = conecta.cursor()

    sql="SELECT time, start_time, finish_time, size_seg, duration, quality, bitrate FROM dash_throughseg"

    try:
            cursor.execute(sql)
            segmentos = cursor.fetchall()

    except MySQLdb.Error, e:
            print "Erro: Banco nao encontrado",e
            menu = raw_input()
            os.system("clear")
            menu()

    segCount=0
    segSum=0
    averageSegmentSum = 0

    for seg in segmentos:
            sizeSeg = float(seg[3])
            bitrate = int(seg[6])
            if bitrate == 3700:
                segSum += sizeSeg
                segCount += 1

    averageSegmentSum += float(segSum)/float(segCount)

    print "SegmentoMedio: %f"%float(averageSegmentSum)

#-------Programa Principal------
def menu():

    os.system("clear");
    print "==================================="
    print "======= QoE Metrics ========"
    print "==================================="


    conecta = conectaBanco()
    AverageHighSegmentSize(conecta)


if __name__=='__main__':
    menu()