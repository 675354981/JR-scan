import os
import subprocess
from termcolor import cprint

class rdp_code_execution_BaseVerify():

    def __init__(self,url):
        current_abs_path = os.path.abspath(__file__)
        current_abs_path_dir = os.path.dirname(current_abs_path)
        self.poc = os.path.abspath(current_abs_path_dir) + '/0708detector.exe'
        self.url=url

    def run(self, port='3389'):
        command = self.poc + ' -t ' + self.url + ' -p ' + port
        result = subprocess.getoutput(command)
        try:
            if 'WARNING: SERVER IS VULNERABLE' in result:
                cprint("[+]存在RDP远程代码执行漏洞", "green")
                return True
            else:
                cprint("[-]不存在RDP远程代码执行漏洞", "white", "on_grey")
        except:
            cprint("[-] " + __file__ + "====>可能不存在漏洞", "cyan")

if __name__ == '__main__':
    rdp=RDP_CodeExecution_BaseVerify('119.23.243.224')
    rdp.run()
