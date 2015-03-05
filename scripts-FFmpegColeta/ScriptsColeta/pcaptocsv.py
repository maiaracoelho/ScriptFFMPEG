'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#this program converts a set of pcap files to a set of csv files

import os
import time
import string
import csv
from operator import itemgetter

def pcaptocsv():
        try:
            print "Please wait, Conversion is going on..."
            os.system("tshark -r %s.pcap -R 'http.request.method=='GET'' -T fields -e frame.number -e frame.time_relative -e http.request.full_uri -e ip.src -e ip.dst -E separator=, > %s.csv"%(input_path+pcap_file_input, path_output_csv+"/"+csv_file_output))
            print "tshark -r %s.pcap -R 'http.request.method=='GET'' -T fields -e frame.number -e frame.time_relative -e http.request.full_uri -e ip.src -e ip.dst -E separator=, > %s.csv"%(input_path+pcap_file_input, path_output_csv+"/"+csv_file_output)
            print "Conversion Successful, Check file on Desktop\n"            
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"


arq=open("entrada_diretorio_captura.txt","r")

input_path = arq.readline()
input_path = input_path.rstrip()
pcap_files = os.listdir(input_path)

path_output_csv=input_path+"csv_files"
os.mkdir(path_output_csv)

for pcap_file in pcap_files:
    name = pcap_file.split(".")
    
    pcap_file_input= name[0]
    csv_file_output= name[0]
    pcaptocsv()
    
