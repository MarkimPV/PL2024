import ply.lex as lex
import json
import re

moeda_inserida = False
saldo = 0
seleciona_flag = False

def changeParameters(mode,bool):
    global moeda_inserida
    global seleciona_flag
    if mode == "ms":
        moeda_inserida = bool
        seleciona_flag = bool
    elif mode == "m":
        moeda_inserida = bool
    elif mode == "s":
        seleciona_flag = bool

def calculaTroco():
    troco = []
    moedas = [200,100,50,20,10,5,2,1]
    count = 0
    global saldo
    saldo_centimos = saldo*100
    while(count <8):
        if(saldo_centimos//moedas[count] > 0):
            troco.append((saldo_centimos//moedas[count]))
            saldo_centimos %= moedas[count]
        else:
            troco.append(0)
        count +=1
    saldo = 0
    return troco
            
file =  open("lista.json",'r+',encoding='utf-8')
data = json.load(file)


tokens = (
    'LISTAR',
    'MOEDA',
    'VALOR',
    'SELECIONAR',
    'ITEM',
    'SAIR'
)


t_ignore = ', \t\n'

def t_MOEDA(t):
    r'MOEDA'
    changeParameters("m",True)
    return t

def t_VALOR(t):
    r'1e|2e|50c|5c|10c|20c|1c|2c'
    changeParameters("s",False)
    global moeda_inserida
    global saldo
    if moeda_inserida:
        if re.fullmatch(r"\d+e",t.value):
            saldo += int(re.findall(r'\d+',t.value)[0])
        else:
            saldo += (int(re.findall(r'\d+',t.value)[0]))/100
        return t
    else:
        t_error(t)
        t.lexer.skip(1)

def t_LISTAR(t):
    r'LISTAR'

    changeParameters("ms",False)
    print("{:<4} | {:<20} | {:<5} | {:<6}".format("cod", "nome", "quant", "preço"))
    print("-" * 43)
    for item in data["stock"]:
        print("{:<4} | {:<20} | {:<5} | {:<6}".format(item["cod"], item["nome"], item["quant"], item["preco"]))
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    changeParameters("m",False)
    changeParameters("s",True)
    return t

def t_ITEM(t):
    r'[A-Z]\d+'
    changeParameters("m",False)
    global seleciona_flag
    global saldo
    if(seleciona_flag):
        for item in data["stock"]:
            if item["cod"] == t.value:
                if item["quant"] > 0:
                    if saldo >= item["preco"]:
                        saldo -= item["preco"]
                        item["quant"] -= 1
                        print(f"maq: Pode retirar o produto dispensado {item["nome"]}")
                        print(f"maq: Saldo = {saldo}")
                    else :
                        print("maq: Saldo insufuciente para satisfazer o seu pedido")
                        print(f"Saldo = {saldo}; Pedido = {item["preco"]}")
                    

                else:
                    print("Produto indisponivel")
        return t
    else:
        changeParameters("s",False)
        t_error(t)
        t.lexer.skip(1)

def t_SAIR(t):
    r'SAIR'
    if(saldo>0):
        moedas = ["2e","1e","50c","20c","10c","5c","2c","1c"]
        out = []
        troco = calculaTroco()
        count = 0
        while(count<8):
            if troco[count] > 0:
                out.append(f'{troco[count]} x {moedas[count]}')
            count+=1
        out = ", ".join(out)
                
        print(f"maq: Pode retirar o troco: {out}.")
    print("maq: Até à próxima")




def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()


lexer.input("MOEDA 2e, 1e, 5c")


while line := input():
    lexer.input(line)
    while tok := lexer.token():
        pass
    print(f'MAQ: Saldo = {saldo}')
