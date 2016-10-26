import time
import os
import sys
import string
import math
from datetime import datetime, timedelta
from operator import itemgetter
import json


def arqToList():
    
    rep={}
    arq = open("/home/dash/Dropbox/DocumentacaoEmpresa/experimentos/testeUFAM1.json")
    representations = arq.readlines()
    arq.close()
    
    json_data = json.loads(open('/home/dash/Dropbox/DocumentacaoEmpresa/experimentos/testeUFAM1.json').read())
    
    return json_data
        
#-------Programa Principal------    
def menu():
    
    
            
    print arqToList()
    
    
    
if __name__=='__main__':
    menu()