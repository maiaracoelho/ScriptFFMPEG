#!/usr/bin/env python
import math
import os

def unfairnessToFairness():
    unfairnessNumbers = str(raw_input("\nDigite o(s) Indice(s) de Injustica separados por espaco: "))
    unfairnessNumbers = map(float, unfairnessNumbers.split())
    
    for i in range(0,len(unfairnessNumbers)):
        unfairnessNumber = unfairnessNumbers[i]
        fairnessNumber = (unfairnessNumber + 1.0)*(unfairnessNumber + 1.0)
        print "FairnessNumber of %f: %f"%(unfairnessNumbers[i], fairnessNumber)
        
        
def menu():
    os.system("clear");
    print "==================================="
    print "======= QoE Metrics ========"
    print "==================================="
    opcao = raw_input("Escolha opcao desejada\n\n[1] - Converter Injustica em Justica\n[7] - Sair")
 
    try:
        opcao = int(opcao)
        if opcao<1 or opcao>7:
            os.system("clear");
            print "OPCAO INVALIDA: Verifique o valor digitado"
            time.sleep(2)
            menu()
    except:
        os.system("clear");
        print "OPCAO INVALIDA: Verifique o valor digitado"
        time.sleep(2)
        menu()
 
    if opcao == 1:
        unfairnessToFairness()
 
    elif opcao == 7:
        sys.exit()

if __name__=='__main__':
    menu()