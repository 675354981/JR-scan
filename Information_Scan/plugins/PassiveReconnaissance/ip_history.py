import re
from Information_Scan.Requests import Requests
from Information_Scan.iscdn import iscdn


def ipinfo(host):   #cdn列表
    out = []
    if not re.search(r'\d+\.\d+\.\d+\.\d+', host):  #不是IP形式的
        req = Requests()
        # noinspection PyBroadException
        try:
            r = req.get('https://viewdns.info/iphistory/?domain={}'.format(host))  #各地DNS
            result = re.findall(r'(?<=<tr><td>)\d+\.\d+\.\d+\.\d+(?=</td><td>)', r.text, re.S | re.I)
            if result:
                for i in result:
                    if iscdn(i):  #是CDN服务器
                        out.append(i)
        except Exception:
            pass

    return out
