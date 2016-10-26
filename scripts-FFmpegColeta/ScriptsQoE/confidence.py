import time
import os
import sys
import string
import math
from datetime import datetime, timedelta
from operator import itemgetter
from math import sqrt

CONFIDENCE_COEFFICIENT = 1.96 #para um intervalo de 95%


def average(numbers):
    
    sum = 0
    av = 0
    count = 0
    for num in numbers:
        sum += num
        count +=1
        
    return sum/count

def stand_deviation(av, numbers):
    
    sub = 0
    sum = 0
    count = 0
    for  num in numbers:
        sub = num - av 
        sub_pot = sub * sub 
        sum += sub_pot
        count += 1
    sd = sum/count
    return sqrt(sd)
        
def error_margin(sd, n):
        
    div = sd/sqrt(n)
    return CONFIDENCE_COEFFICIENT * div
    

#-------Programa Principal------    
def menu():
    numbers = str(raw_input("\nDigite o(s) numeros a serem calculados separados por espaco: "))
    numbers = map(float, numbers.split())
    
    av = average(numbers)
    
    sd = stand_deviation(av, numbers)
    
    se = error_margin(sd, len(numbers))
    
    print "average is: %f"%av
    print "stand_deviation is: %f"%sd
    print "Margin Of Error is: %f"%se
    print "Min Average: %f"%(av-se)
    print "Max Average: %f"%(av+se)
    
    
    
    
if __name__=='__main__':
    menu()