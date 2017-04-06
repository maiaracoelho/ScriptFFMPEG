#!/usr/bin/python

import httplib2
import json


uri = "http://encoding.akirymedia.com:9080/api"
token = 'OGVjYTNhNzg2YzRiOWQ3YTkyYzA3N2QyNGIxODliMjEyYWNkOGEyYWExMDRjOGViZTYzMzVkNzczNDVlODYzMg=='



def getLogs(date=None):

            headers = {
                       'Authorization': 'Bearer ' + token
            }
            url = uri + 'logs/' + str(date)

            http = httplib2.Http(disable_ssl_certificate_validation=True)
            headers, content = http.request(url, "GET", headers=headers)

            if headers.status == 200:
                return json.loads(content)
            else:
                return None
            


def main():
    
    date = input("Digite a data no formato dd-mm-yyyy: ")
    logsList = getLogs(date=date)
    
    if logsList is None:
            print("Is None")
    else:
        print logsList
        for log in logsList:
            pass
    

if __name__ == '__main__':
    main()
