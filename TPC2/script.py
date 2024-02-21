import re

# #
def convertHead(string):
    num = len(re.findall('^#+ ',string)[0]) if len(re.findall('^#+ ',string)) else 0
    return f'{re.sub('^#+ ',f'<h{num-1}>\n',string)}</h{num-1}>\n' if num !=0 else string

def convertBold(string):
    return re.sub(r'\*{2}(.*)\*{2}',r' <b>\1</b>\n',string)

def convertItalic(string):
    return re.sub(r'( |)\*([a-zA-Z\d]+)\*',r' <i>\2</i>\n',string)

def convertList(string,opt):
    str1 = string
    if opt == 'init':
        str1 = re.sub(r'^\d\. (.*)',r'<li>\1</li>',string)
        str1 = re.sub(r'(<li>.*</li>\n)+',r'<ol>\n\1',str1)
    elif opt == 'inter':
        str1 = re.sub(r'^\d\. (.*)',r'<li>\1</li>',string)

    return str1

def convertLink(string):
    return re.sub(r' \[(.*)\]\((.*)\)',r' <a href="\2">\1</a>',string)

def convertImage(string):
    return re.sub(r'!\[(.*)\]\((.*)\)',r'<img src="\2" alt="\1"/>',string)


def main():
    html = ''
    file1 = open("html.html",'w')
    listPos = 0
    with open('markdown-sample.md','r') as file:
        for l in file:
            line = l
            if listPos == 0:
                l = convertList(l,'init')
                if l != line:
                    listPos = 1
            elif listPos == 1:
                l = convertList(l,'inter')
                if l == line:
                    l += '</ol>\n'
                    listPos = 0
            l = convertHead(l)
            l = convertBold(l)
            l = convertItalic(l)
            l = convertLink(l)
            l = convertImage(l)
            file1.write(l)
    file1.close()

main()

