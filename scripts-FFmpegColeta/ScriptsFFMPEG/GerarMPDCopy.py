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
        comando = "MP4Box -dash %d -frag 1000 -dash-profile %s -subsegs-per-sidx 2 -segment-name onDemand_"%(sec_time, profile)
        comando = comando+"%s"
        print comando+" -out %s.mpd %s"%(path_sec+"/"+mpd, out_files)

        try:
            print "Please wait, Conversion is going on..."
            os.system(comando+" -out %s.mpd %s"%(path_sec+"/"+mpd, out_files))
            print "Conversion Successful, Check file on Desktop\n"
            
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"

arq=open("entrada_diretorios.txt","r")
path = arq.readline()
path = path.rstrip()
out_files=[]
granularities=["alta","baixa"]
profiles=['onDemand']
crfs=[12,48]
fpss=[7,30]
secs=[5]
i=0
#Criar a hierarquia de diretorios
for granul in granularities:
    path_granul=path+str(granul)
    for crf in crfs:
        path_crf=path_granul+"/CRF-"+str(crf)
        for fps in fpss:
            path_fps=path_crf+"/FPS"+str(fps)
       	    out_file = os.listdir(path_fps)
            
            for i in range(0,len(out_file)):
                if i!=0:
                    file = out_file[i].split("_")
                    #print file
    		    if len(file)!=2:
                        video_bitrate = file[1]
                        band = (int(video_bitrate)+100)*1000
                        out_file[i] = out_file[i]+"#video:bandwidth="+str(band) 
                        print band  
            out_base_path = " "+path_fps+"/"
            out_files = out_base_path+out_base_path.join(out_file)
            for profile in profiles:
                path_profile=path_fps+"/"+profile
                #os.mkdir(path_profile)
                for sec in secs:
                    if sec==5: sec_time = 5000
                    elif sec==10: sec_time = 10000
                    elif sec==15: sec_time = 15000
                    path_sec=path_profile+"/"+str(sec)+"s"
                    #os.mkdir(path_sec)
                    mpd = profile+"_"+str(sec)+"s"
                    tompd()
arq.close()
