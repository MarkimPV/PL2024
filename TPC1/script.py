"""

Info a captar

Modalidades
Idades por facha etária
Resultado (Verificar os que são aptos) - Precisoa saber total de atletas

Ignorar: 1,2,3,7,9,10,11
Em conta: 4,5,6(Nome,Idade), 8(Modalidade), 12(Aprovação)


"""

import os


faixa_etaria = {}
modalidades = set()
aprovados = 0
count = 0

file = open("emd.csv","r",encoding="utf-8")
file.readline() # Ignorar primeira linha

def faixaEtaria(idade):
    return idade // 5 * 5

for line in file: #Para cada linha do csv
    count +=1     #Conta linhas (elementos)
    content = line.split(',') #Seprara os elementos da linha
    modalidades.add(content[8]) #Adiciona a modalidade a um set
    faixa = f"{faixaEtaria(int(content[5]))} - {faixaEtaria(int(content[5]))+4}" #Calcula a faixa etaria
    if faixa not in faixa_etaria:   #Cria engtrada da faixa etaria se nao existe
        faixa_etaria[faixa] = []
    faixa_etaria[faixa].append(content[3] + ' ' + content[4]) #Adiciona elemento ao à entrada correspondente
    if(content[12] == "true\n"):    #Verifica se é apto
         aprovados += 1 


file.close()

print(sorted(modalidades))
print(f"Aprovados: {(aprovados/count)*100}%\nNão Aprovados: {100-(aprovados/count)*100}%")
for key,value in faixa_etaria.items():
    print(f"[{key}] -> {value}\n")











