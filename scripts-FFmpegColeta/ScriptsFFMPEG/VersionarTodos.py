'''
Created on 16/07/2014

@author: dashclient
'''
#!/usr/bin/env python
#python video converter
import os
import time
import string

# eh importante observar que a taxa de bits total eh a soma do bitrate de audio e do bitrate de video 
def tomp4():
        try:
            print "Please wait, Conversion is going on..."
            os.system("ffmpeg -i %s -codec:v libx264 -profile:v baseline -r %d -minrate %dk -maxrate %dk -bufsize %dk -s %dx%d -threads 0 %s.mp4"%(input_path+input_file, fps, int(video_bitrate), int(video_bitrate), int(video_bitrate), int(scale1), int(scale2), path_fps+"/"+output_file))
            print "ffmpeg -i %s -codec:v libx264 -profile:v baseline -r %d -minrate %dk -maxrate %dk -bufsize %dk -s %dx%d -threads 0 %s.mp4"%(input_path+input_file, fps, int(video_bitrate),  int(video_bitrate),  int(video_bitrate), int(scale1), int(scale2), path_fps+"/"+output_file)
            print "Conversion Successful, Check file on Desktop\n"
        except:
            print "Conversion Unsuccessful, Some required files are missing\n"

arq=open("entrada_script_ffmpeg_baixa.txt","r")
linha1 = arq.readline()
input_path,file_name,input_file,output_path = linha1.split()

fpss=[7,30]
output_files=[]
linhas = arq.readlines()
path_videos= output_path+"videos_versionados/"
os.mkdir(path_videos)

for fps in fpss:
         path_fps=path_videos+"FPS"+str(fps)
         os.mkdir(path_fps)
         for linha in linhas:
              video_bitrate, scale1, scale2= linha.split()
              output_file = file_name+"_"+str(video_bitrate)+"_fps"+str(fps)
              tomp4()
arq.close()
    
