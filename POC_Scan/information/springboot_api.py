#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: spring boot 路径泄露
referer: http://blog.csdn.net/u011687186/article/details/73457498
author: Lucifer
description: SpringBoot默认API会暴露出敏感接口
'''
import sys
import requests
import warnings
from termcolor import cprint

class springboot_api_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        payload = "/mappings"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)

            if "resourceHandlerMapping" in req.text and r"springframework.boot.actuate" in req.text:
                cprint("[+]存在spring boot api路径泄露...(敏感信息)"+"\tpayload: "+vulnurl, "green")
                return True
            else:
                cprint("[-]不存在springboot_api漏洞", "white", "on_grey")

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = springboot_api_BaseVerify(sys.argv[1])
    testVuln.run()
