import sys
import re

def tokenize(code):
    token_specification = [
        ('NUM',   r'\d+'),         
        ('KEYWORD', r'SELECT|FROM|WHERE'),      
        ('VAR',   r'[_A-Za-z]\w+'),     
        ('COMP',   r'=|<=|>='),                         
        ('SEP', r','),
        ('NEWLINE',  r'\n'),           
        ('SKIP',     r'[ \t]+'), 
        ('ERRO', r'.'),               
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    reconhecidos = []
    linha = 1
    mo = re.finditer(tok_regex, code)
    for m in mo:
        dic = m.groupdict()
        t = None
        if dic['NUM'] is not None:
            t = ("NUM", int(dic['NUM']))
        elif dic['VAR'] is not None:
            t = ("VAR", dic['VAR'])
        elif dic['COMP'] is not None:
            t = ("COMP", dic['COMP'])
        elif dic['KEYWORD'] is not None:
            t = ("KEYWORD", dic['KEYWORD'])
        elif dic['SEP'] is not None:
            t = ("SEP", ",")
        elif dic['SKIP'] is not None:
            pass
        else:
            t = ("ERRO", m.group())
        if t:
            reconhecidos.append(t)

    return reconhecidos


for linha in sys.stdin:
    for tok in tokenize(linha):
        print(tok)