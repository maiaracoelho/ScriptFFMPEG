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
            os.system("ffmpeg -i %s -codec:a libfdk_aac -b:a %dk  %s.mp4"%(input_path+input_file, int(audio_bitrate), path_fps+"/"+output_file))
            print "ffmpeg -i %s -codec:a libfdk_aac -b:a %dk  %s.mp4"%(input_path+input_file, int(audio_bitrate), path_fps+"/"+output_file)
            print "Conversion Successful, Check file on Desktop\n"            
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"
   

arq=open("entrada_script_ffmpeg_audio.txt","r")

linha1 = arq.readline()
input_path,file_name,input_file,output_path, audio_bitrate = linha1.split()
fpss=[7, 30]

for fps in fpss:
            path_fps=output_path+"FPS"+str(fps)
            output_file = file_name+"_"+str(audio_bitrate)+"_k"
            tomp4()
arq.close()

    
