import pyfiglet   #ascii艺术字体
from lib.bcolors import Bcolors
import time
import sys

def banner():   #载入界面
    ascii_banner = pyfiglet.figlet_format("JinRong")    #使用字符组成ASCII艺术图片
    print(Bcolors.RED + ascii_banner + Bcolors.ENDC)

def usage():
        s = '帮助:\n'
        s += '    [1]Information_Scan         信息收集\n'
        s += '    [2]POC_Scan                 POC扫描\n'
        s += '    [3]AWVS_Check               AWVS检测\n'
        s += '    [4]H5_Create                结果展示\n'
        s += '    [5]Help                     帮助\n'
        s += '    [6]Exit                     退出'
        print(Bcolors.BLUE + s + Bcolors.ENDC)

def console(plugins, domain, text):     #目标检测展示界面    已定义  目标  内容  console('PING', host, "is not alive\n")
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    timestamp = Bcolors.BLUE + '[' + timestamp + ']' + Bcolors.ENDC
    plugins = Bcolors.RED + plugins + Bcolors.ENDC
    text = Bcolors.GREEN + text + Bcolors.ENDC
    sys.stdout.write(timestamp + ' - ' + plugins + ' - ' + domain + '    ' + text)

if __name__ == '__main__':
    banner()