import re

with open('file.txt','r') as file:
    flag = False
    count = 0
    for line in file:
        c = re.findall(r'(on|off|\d+|=)',line,flags=re.I)
        for element in c:
            if element.lower() == 'on':
                flag = True
            elif element.lower() == 'off':
                flag = False
            elif element == '=':
                print(count)
            else:
                if flag:
                    count+= int(element)
    

            