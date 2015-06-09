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
path_videos= path+"videos_versionados_netflix/"
profiles=['onDemand']
granularities=["1000-3600"] 
video_bitrates = [1000, 1400, 1500, 1600, 1750, 2350, 3600]
fpss=[30]
secs=[2,4]
i=0

#Criar a hierarquia de diretorios
for granul in granularities:
    path_granul=path+str(granul)
    os.mkdir(path_granul)
    audio_bitrate = 100
    
    for fps in fpss:
        out_files=[]
        files=[]
        
                
        path_fps=path_granul+"/FPS"+str(fps)
        os.mkdir(path_fps)
        
        #arquivo de audio para ser o primeiro da lista de videos
        band = audio_bitrate*1000
        out_file = "sintelA_"+str(audio_bitrate)+"_k.mp4#video:bandwidth="+str(band)
        files.append(out_file)
            
        for video_bitrate in video_bitrates:
            band = video_bitrate*1000
            out_file = "sintelV_"+str(video_bitrate)+"_fps"+str(fps)+"_720.mp4#video:bandwidth="+str(band)
            files.append(out_file)
            
        print files
              
        out_base_path = " "+path_videos+"FPS"+str(fps)+"/"
            
        out_files = out_base_path+out_base_path.join(files)
        for profile in profiles:
            path_profile=path_fps+"/"+profile
            os.mkdir(path_profile)
            for sec in secs:
                if sec==2: sec_time = 2000
                if sec==4: sec_time = 4000
                if sec==5: sec_time = 5000
                path_sec=path_profile+"/"+str(sec)+"s"
                os.mkdir(path_sec)
                mpd = profile+"_"+str(sec)+"s"
                tompd()
            
arq.close()
