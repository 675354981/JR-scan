import re
import sys
from lib.bcolors import Bcolors
from lib.cli_output import console
from POC_Scan.information.informationmain import *
from POC_Scan.cms.cmsmain import *
from POC_Scan.pocdb import pocdb_pocs
from POC_Scan.system.systemmain import *

def split_string(strLine):
    pattern = r"[a-z_]+BaseVerify"
    return str(re.findall(pattern, strLine)).replace("_BaseVerify", "").replace("['","").replace("']","")

def show_poc():
    # 列出Information POC名称
    pocclass = pocdb_pocs('')
    informations = pocclass.informationpocdict
    print(Bcolors.RED+"\t\t\tInformation POC"+Bcolors.ENDC)
    for information in informations:
        print("|" + information + "\t|\t" + split_string(str(informations.get(information))))
        print( "|-------------------------------------------------------------------------------------------------------------|")
    print("\r")

    # 列出CMS POC名称
    pocclass = pocdb_pocs('')
    cmsclass = pocclass.cmspocdict
    print(Bcolors.RED+"\t\t\tCMS POC"+Bcolors.ENDC)
    for cms in cmsclass:
        print("|" + cms + "\t|\t" + split_string(str(cmsclass.get(cms))))
        print("|-------------------------------------------------------------------------------------------------------------|")
    print("\r")

    # 列出SYSTEM POC名称
    pocclass = pocdb_pocs('')
    systemclass = pocclass.systempocdict
    print(Bcolors.RED+"\t\t\tSYSTEM POC"+Bcolors.ENDC)
    for system in systemclass:
        print("|" + system + "\t|\t" + split_string(str(systemclass.get(system))))
        print("|-------------------------------------------------------------------------------------------------------------|")
    print("\r")

def search(keywords):
        count = 0
        print(Bcolors.MAGENTA+"搜索结果: "+Bcolors.ENDC)
        with open("POC_Scan/pocdb.py", "r", encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.find(keywords) != -1:
                    count += 1
                    line = line.split(":")
                    linename = line[0].rstrip('"').lstrip('"')
                    linepoc = line[1].replace("_BaseVerify(url),", "")
                    searchstr = "[" + str(count) + "]漏洞名: " + linename + "=======>" + linepoc
                    print(searchstr)

def poc_use():
    poc_class = pocdb_pocs("")
    informationpocs = len(poc_class.informationpocdict)
    cmspocs = len(poc_class.cmspocdict)
    systempocs = len(poc_class.systempocdict)
    total = cmspocs + systempocs + informationpocs
    print("|---------------------------------------|",)
    print("| Information漏洞POC个数:          " + str(informationpocs), "   |")
    print("| CMS漏洞POC个数:                  " + str(cmspocs), "  |")
    print("| SYSTEM漏洞POC个数:               " + str(systempocs), "  |")
    print("| 总漏洞POC个数:                   " + str(total), "  |")
    print("|---------------------------------------|",)

    s = '帮助:\n'
    s += '    [1]show poc         POC展示\n'
    s += '    [2]search poc       POC查询\n'
    s += '    [3]use poc          POC利用\n'
    s += '    [4]back menu        返回上级菜单\n'
    print(Bcolors.BLUE + s + Bcolors.ENDC)

def use(poc,target):
    vary=[]

    if re.search(r'\.txt$',target):
        poc_class = pocdb_pocs("")
        alldict = dict()

        tmpdict = poc_class.informationpocdict.copy()
        alldict.update(tmpdict)
        tmpdict = poc_class.cmspocdict.copy()
        alldict.update(tmpdict)
        tmpdict = poc_class.systempocdict.copy()
        alldict.update(tmpdict)

        for keyword in alldict.values():
            if str(keyword).find(poc) != -1:
                break
        filepath = target
        sys.stdout.write("\033[1;35m[+] 加载poc: [" + keyword.__module__ + "]\033[0m\n")
        with open(filepath) as f:
            for line in f.readlines():
                line = line.strip()
                sys.stdout.write("\033[1;35m[+] 发送payload..\033[0m\n")
                sys.stdout.write("\033[1;35m[+] 正在攻击.." + line + "\033[0m\n")
                keyword.url = line
                if keyword.run():
                    vary.append(line)

    else:
        poc_class = pocdb_pocs(target)
        alldict = dict()

        tmpdict = poc_class.informationpocdict.copy()
        alldict.update(tmpdict)

        tmpdict = poc_class.cmspocdict.copy()
        alldict.update(tmpdict)

        tmpdict = poc_class.systempocdict.copy()
        alldict.update(tmpdict)

        for keyword in alldict.values():
            if str(keyword).find(poc) != -1:
                break
        sys.stdout.write("\033[1;35m[+] 加载poc: [" + split_string(str(keyword)) + "]\033[0m\n")
        sys.stdout.write("\033[1;35m[+] 发送payload..\033[0m\n")
        sys.stdout.write("\033[1;35m[+] 正在攻击.." + target + "\033[0m\n")
        if keyword.run():
            vary.append(target)

    return vary

if __name__ == '__main__':
    poc_use()
    while True:
        command,keywords = input('[JR/POC_Scan/]>>').split()
        if command == 'search'and keywords:
            search(keywords)
        if command == "show" and keywords == 'poc':
            show_poc()
        if command == 'use' and keywords:
            target=input('[JR/POC_Scan/Set_Target]>>')
            use(keywords,target)