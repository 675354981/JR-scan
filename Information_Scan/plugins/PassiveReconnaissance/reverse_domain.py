import requests
import json
import tldextract  #tldextract准确地从URL的域名和子域名分离通用顶级域名或国家顶级域名。
import re
from lib.cli_output import console
from Information_Scan.random_header import get_ua

def reverse_domain(host):   # 查询旁站
    result = []
    data = {"remoteAddress": "{0}".format(host), "key": ""}
    header = get_ua()   #自定义headers头
    try:
        r = requests.post('https://domains.yougetsignal.com/domains.php',
                          headers=header,
                          data=data,
                          timeout=5,
                          verify=False)
        text = json.loads(r.text)    #返回json格式
        domain = tldextract.extract(host)  #将URL分割，获得各个域名  http://forums.news.cnn.com/  subdomain='forums.news', domain='cnn', suffix='com'
        for i in text.get('domainArray'):
            url = i[0]
            if url != host:   #看看域名是否一致
                if tldextract.extract(url).domain == domain.domain:   #二级域名比较  top.baidu.com    m.baidu.com
                    result.append(url)   #二级域名添加
                elif re.search(r'\d+\.\d+\.\d+\.\d+', url):   
                    result.append(url)  #IP添加
    except:
        try:
            r = requests.get('http://api.hackertarget.com/reverseiplookup/?q={}'.format(host),
                             headers=get_ua(),  #自定义的headers头
                             timeout=4,
                             verify=False)
            if '<html>' not in r.text and 'No DNS A records found for' not in r.text:    #No DNS A records found for 119.3.60.210   其余情况就是出现了域名
                text = r.text
                for _ in text.split('\n'):
                    if _:
                        result.append(_)  #添加域名
            else:
                result = []
        except:
            pass
    if len(result) < 20:
        if result:
            for i in result:
                console('reverse_domain', host, i + '\n')   #旁站进行展示
        else:
            console('reverse_domain', host, 'None\n')
        return result
    else:
        console('reverse_domain', host, 'The maximum number of domain names exceeded (20)\n')
        return ['The maximum number of reverse_domain names exceeded (20)']

