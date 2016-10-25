import time
import os
import sys
import string
import math
from datetime import datetime, timedelta
from operator import itemgetter
from math import sqrt


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
    print sd
    return sqrt(sd)
        

#-------Programa Principal------    
def menu():
    numbers = str(raw_input("\nDigite o(s) numeros a serem calculados separados por espaco: "))
    numbers = map(float, numbers.split())
    
    av = average(numbers)
    
    sd = stand_deviation(av, numbers)

    print "average is: %f"%av
    print "stand_deviation is: %f"%sd
    
if __name__=='__main__':
    menu()