#!/usr/bin/python

import httplib2
import json
import ast
from operator import itemgetter
from itertools import izip

uri = "http://encoding.akirymedia.com:9080/api/v1.0"
token = 'OGVjYTNhNzg2YzRiOWQ3YTkyYzA3N2QyNGIxODliMjEyYWNkOGEyYWExMDRjOGViZTYzMzVkNzczNDVlODYzMg=='
pathArqs = "/home/maiara/Dropbox/DocumentacaoEmpresa/experimentos"

def getLogs(date=None):

            headers = {
                       'Authorization': 'Bearer ' + token
            }
            url = uri + '/logs/' + str(date)

            http = httplib2.Http(disable_ssl_certificate_validation=True)
            headers, content = http.request(url, "GET", headers=headers)

            if headers.status == 200:
                return json.loads(content)
            else:
                return None


def fromListToList(logsList):

    dictLogs = {}

    for i in range(0,len(logsList)):
        for j in range(0,len(logsList[i])):
            log = logsList[i][j]

            jobId = log["object"]["timeline"]["job"]
            category = log["category"]
            event = log["event"]
            time = log["object"]["timeline"]["timestamp"]
            filesize = None
            if event == "download_completed":
                filesize = log["filesize"]

            #dictLog={jobId:dict={"mover_inicial_time","mover_final_time","transcode_inicial_time","transcode_final_time","sendToS3_inicial_time", "sendToS3_final_time", "filesize"
            if not dictLogs.has_key(jobId):
                dictLogs[jobId] = {"mover_inicial_time": None, "mover_final_time": None, "transcoder_inicial_time": None, "transcoder_final_time": None, "sendToS3_inicial_time": None, "sendToS3_final_time": None, "filesize": None}

            if category == "mover":
                if event == "download_started":
                    dictLogs[jobId]["mover_inicial_time"] = time
                if event == "download_completed":
                    dictLogs[jobId]["mover_final_time"] = time
                    dictLogs[jobId]["filesize"] = filesize
            if category == "transcoder":
                if event == "transcode_started":
                    dictLogs[jobId]["transcoder_inicial_time"] = time
                if event == "transcode_completed":
                    dictLogs[jobId]["transcoder_final_time"] = time
            if category == "sendToS3":
                if event == "sendS3_started":
                    dictLogs[jobId]["sendToS3_inicial_time"] = time
                if event == "sentS3_success":
                    dictLogs[jobId]["sendToS3_final_time"] = time

    return dictLogs


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

    dates = str(raw_input("Entre com as datas  no formato dd-mm-yyyy separadas por espaco: "))
    dates = list(dates.split(" "))
    logsList = []

    for date in dates:
        logsListDay = ast.literal_eval(json.dumps(getLogs(date=date)))
        logsList.append(logsListDay)

    if not logsList is None:
        dictEncoder = fromListToList(logsList)
        listEncoder = sorted(dictEncoder.iteritems(), key=lambda (x, y): y['filesize'])
        generateArqToTxtAll(listEncoder)

if __name__ == '__main__':
    main()
