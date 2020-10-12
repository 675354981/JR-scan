#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: svn源码泄露扫描
referer: unknown
author: Lucifer
description: 忘记了删除.svn目录而导致的漏洞。
'''
import re
import sys
import requests
import warnings
from termcolor import cprint

class svn_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/.svn/entries"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False, allow_redirects=False)
            try:
                contents = str(req.text).split('\x0c')
                pattern = re.compile(r'has-props|file|dir')
                for content in contents:
                    match = len(pattern.search(content).group(0))
                    if req.status_code == 200 and match > 0:
                        cprint("[+]存在svn源码泄露漏洞...(高危)\tpayload: "+vulnurl, "red")
                        return True
                        break
                    else:
                        cprint("[-]不存在svn_check漏洞", "white", "on_grey")
            except:
                cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")

        except:
            cprint("[-] "+__file__+"====>可能不存在漏洞", "cyan")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = svn_check_BaseVerify(sys.argv[1])
    testVuln.run()
