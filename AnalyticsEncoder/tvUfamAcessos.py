#!/usr/bin/python

import httplib2
import json
import ast
from operator import itemgetter
from itertools import izip
import os

pathArqs = "/home/dash/Dropbox/DocumentacaoEmpresa/experimentos/logsTvUfam"


def counterAccessByDay(linhas):

    logs = []
    mobileAccessDay = 0
    desktopAccessDay = 0 

    for linha in linhas:
            linha = linha.split(":") 
            del linha[0:3]                     
            linha = ':'.join(linha)
            #linha = ast.literal_eval(linha)
            d = json.loads(linha)
            if "Fingerprint" in d.keys():
                print linha
                
                dictFingerprint = list(d["Fingerprint"])[0]
                
                dictTimeline = dictFingerprint["timeline"]
                if not "tvufam" in dictTimeline["appId"]:
                    continue
                if dictFingerprint["deviceType"] == "mobile":
                    mobileAccessDay+=1
                else:
                    desktopAccessDay+=1
                
    return mobileAccessDay, desktopAccessDay


def generateCountsDevice(linhas, dict):

    
    for linha in linhas:
            linha = linha.split(":") 
            del linha[0:3]                     
            linha = ':'.join(linha)
            #linha = ast.literal_eval(linha)
            d = json.loads(linha)
            if "Fingerprint" in d.keys():
                dictFingerprint = list(d["Fingerprint"])[0]
                dictTimeline = dictFingerprint["timeline"]
                if not "tvufam" in dictTimeline["appId"]:
                    continue
                
                if dictFingerprint["deviceId"] in dict:
                    dict[dictFingerprint["deviceId"]] += 1
                else:
                    dict[dictFingerprint["deviceId"]] = 1 
    
    return dict


def generateArqToTxtAll(listEncoder):

    sum_mover_time = sum_transcoder_time = sum_upload_time = sum_filesize = count = 0

    arq = open(pathArqs + "/experimentoAllDays.txt", 'w')
    arq2 = open(pathArqs + "/experimentoAverages.txt", 'w')

    for encoder in listEncoder:
        job = encoder[0]
        dictItem = encoder[1]

        if (not (dictItem["mover_inicial_time"] is None)
        and not (dictItem["mover_final_time"] is None)
        and not (dictItem["transcoder_inicial_time"] is None)
        and not (dictItem["transcoder_final_time"] is None)
        and not (dictItem["sendToS3_inicial_time"] is None)
        and not (dictItem["sendToS3_final_time"] is None)
        and not (dictItem["filesize"] is None)):

            count += 1

            jobId = delta_mover = delta_transcoder = delta_upload = filesize = None

            jobId = job
            mover_inicial_time = float(dictItem["mover_inicial_time"])
            mover_final_time = float(dictItem["mover_final_time"])
            delta_mover = mover_final_time - mover_inicial_time
            delta_mover = delta_mover
            transcoder_inicial_time = float(dictItem["transcoder_inicial_time"])
            transcoder_final_time = float(dictItem["transcoder_final_time"])
            delta_transcoder = transcoder_final_time - transcoder_inicial_time
            delta_transcoder = delta_transcoder
            sendToS3_inicial_time = float(dictItem["sendToS3_inicial_time"])
            sendToS3_final_time = float(dictItem["sendToS3_final_time"])
            delta_upload = sendToS3_final_time - sendToS3_inicial_time
            delta_upload = delta_upload
            filesize = float(dictItem["filesize"])
            filesize = filesize/1000

            sum_mover_time += delta_mover
            sum_transcoder_time += delta_transcoder
            sum_upload_time += delta_upload
            sum_filesize += filesize

            linha = str(jobId) + " " + str(delta_mover) + " " + str(delta_transcoder)
            linha += " " + str(delta_upload) + " " + str(filesize) + "\n"
            print linha

            arq.write(linha)
    arq.close()

    average_mover_time = sum_mover_time / count
    average_transcoder_time = sum_transcoder_time / count
    average_upload_time = sum_upload_time / count
    average_filesize = sum_filesize / count
    arq2.write(str(count) + " " + str(average_mover_time) + " " + str(average_transcoder_time) + " " + str(average_upload_time) + " " + str(average_filesize) + "\n")
    arq2.close()


def main():

    dictAcessDay = {}
    dictAcessDevice = {}
    filenames = os.listdir(pathArqs)
    totalAccess = 0
    for filename in filenames:
        file = os.path.join(pathArqs, filename)
        arq = open(file, 'r')
        linhas = arq.readlines()
        
        acessMobile, acessDesktop = counterAccessByDay(linhas) 
        dictAcessDay[filename] = acessMobile, acessDesktop
        totalAccess+=(acessMobile + acessDesktop)
        
        dictAcessDevice = generateCountsDevice(linhas, dictAcessDevice) 

        
    print dictAcessDay
    print totalAccess
    print totalAccess/len(dictAcessDay.keys())
    print dictAcessDevice
    print len(dictAcessDevice.keys())
    print totalAccess/len(dictAcessDevice.keys())
    
        #generateTxt() 
    
    

if __name__ == '__main__':
    main()
