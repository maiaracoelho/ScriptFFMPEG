'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#python video converter

import os
import time
import string
import StringIO

def tompd():
        try:
            print "Please wait, Conversion is going on..."
            os.system("MP4Box -dash %d -frag 1000 -dash-profile %s -subsegs-per-sidx 2 -segment-name main-$RepresentationID$ -out %s.mpd %s"%(time, profile, mpd, out_files))
            print "Conversion Successful, Check file on Desktop\n"
            time.sleep(3)
            
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"


profiles=['live','main','onDemand','full']
secs=[2,5,10]
intervs=[[256,1000],[4000,8000]]
arq=open("entrada_diretorios.txt","r")
caminho = arq.readline()
caminho = caminho.rstrip()

#Criar a hierarquia de diretorios
for profile in profiles:
    os.mkdir(caminho+profile)
    for sec in secs:
        os.mkdir(caminho+profile+"/"+str(sec)+"s")
        for interv in intervs:
            interview =  caminho+profile+"/"+str(sec)+"s/"+str(interv[0])+"-"+str(interv[1])+"k"
            os.mkdir(interview)
            print interview
            
     
