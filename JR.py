import sys
import gevent
from gevent import monkey
monkey.patch_all()
from report import gener
from lib.cli_output import banner
from lib.cli_output import usage
from lib.bcolors import Bcolors
from lib.enter import add
from Information_Scan.common import start
from POC_Scan.main import poc_use
from POC_Scan.main import search,show_poc,use
from lib.sqldb import Sqldb
from AWVS_Check.AWVS import awvs

class JR(object):

    def handle(self):   # 进行调度
        try:
            dbname = 'result'
            banner()
            print('-' * 43)
            usage()
            print('-' * 43)
            while True:
                show = input(Bcolors.RED + '[JR]>> ' + Bcolors.ENDC)  # 红色
                if show in ['1','Information_Scan']:
                    target = input(Bcolors.RED + '[JR/Information_Scan/Set_Target]>>' + Bcolors.ENDC)
                    lives=add(target)
                    for i in lives:
                        start(i,dbname)

                elif show in ['2','POC_Scan']:
                    poc_use()
                    while True:
                        command, keywords = input(Bcolors.RED + '[JR/POC_Scan/]>>' + Bcolors.ENDC).split()
                        if command == 'search' and keywords:
                            search(keywords)
                        elif command == "show" and keywords == 'poc':
                            show_poc()
                        elif command == 'use' and keywords:
                            target = input(Bcolors.RED+'[JR/POC_Scan/Set_Target]>>'+Bcolors.ENDC)
                            lives=add(target)
                            for live in lives:
                                for i in use(keywords, live):
                                    Sqldb(dbname).get_vuln(i,keywords)
                        elif command =='back' and keywords == 'menu':
                            break
                        else:
                            print(Bcolors.WARNING + '[-] 提示: 输入错误...' + Bcolors.ENDC)

                elif show in ['3','AWVS_Check']:
                    awvs_check=awvs()
                    awvs_check.usage()
                    while True:
                        command= input(Bcolors.RED + '[JR/AWVS_Check/]>>' + Bcolors.ENDC)
                        if command == 'scan':
                            awvs_check.scan()
                        elif command == "stop":
                            awvs_check.stop()
                        elif command == 'delete':
                            awvs_check.delete()
                        elif command =='view':
                            awvs_check.view()
                        elif command =='back':
                            break
                        else:
                            print(Bcolors.WARNING + '[-] 提示: 输入错误...' + Bcolors.ENDC)

                elif show in ['4','H5_Create']:
                    gener()
                elif show in ['5','Help']:
                    usage()
                elif show in ['6','exit']:
                    break
                elif show == '':
                    pass
                else:
                    print(Bcolors.WARNING + '[-] 提示: 输入错误...' + Bcolors.ENDC)
        except KeyboardInterrupt as e:
            print(e)

if __name__ == '__main__':
    try:
        jr=JR()
        jr.handle()
    except KeyboardInterrupt:
        print('\nCtrl+C Stop running\n')
        sys.exit(0)