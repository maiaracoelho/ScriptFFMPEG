'''
Created on 03/02/2015

@author: dashclient
'''
#!/usr/bin/env python
import math

k_interrup = int(input())
v_interrup = []
v_result = []
v_result2 = []
v_result3 = []
v_sum = []
v_sum2 = []
sum = 0.0
sum2 = 0.0
T = 720.0


print "Considerando a duracao"

for i in range(0, k_interrup):
    #v_interrup.append(i+1)
    v_interrup.append(2.0)

for j in range(len(v_interrup)):
    
    den = math.pow(2.0,j + 1 - 1) 
    div = v_interrup[j]/den
    sum += div
    v_result.append(div)
    v_sum.append(sum)
    
    
print v_interrup
print v_result
print v_sum

print "Considerando a interrupcao"

for l in range(len(v_interrup)):
    
    multi = math.pow(2.0,l - k_interrup) 
    res = multi * v_interrup[l]
    sum2 += res
    v_result2.append(res)
    v_sum2.append(sum2)

print v_interrup
print v_result2
print v_sum2

print "Resultado final"

for i in range(len(v_interrup)):
    result = (v_sum[i] + v_sum2[i])/T
    v_result3.append(result)
    
print v_result3


