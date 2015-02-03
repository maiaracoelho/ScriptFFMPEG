'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#python video converter

import os
import time
import string
   
def tomp4():
        try:
            print "Please wait, Conversion is going on..."
            os.system("ffmpeg -i %s -codec:a libfdk_aac -b:a 100k  %s.mp4"%(input_path+input_file, path_fps+"/"+output_file))
            print "ffmpeg -i %s -codec:a libfdk_aac -b:a 100k  %s.mp4"%(input_path+input_file, path_fps+"/"+output_file)
            print "Conversion Successful, Check file on Desktop\n"            
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"
   

arq=open("entrada_script_ffmpeg_audio.txt","r")

linha1 = arq.readline()
input_path,file_name,input_file,output_path = linha1.split() 
crfs=[12,48]
fpss=[7,30]
granularities=["alta", "baixa"]
for granul in granularities:
    path_granul=output_path+str(granul)
    for crf in crfs:
        path_crf=path_granul+"/CRF-"+str(crf)
        for fps in fpss:
            path_fps=path_crf+"/FPS"+str(fps)
            output_file = file_name+"_100k"
            tomp4()
arq.close()
    
