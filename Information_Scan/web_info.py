import chardet  #用来检测编码格式
from Information_Scan.plugins.ActiveReconnaissance.osdetect import osdetect
from Information_Scan.url import parse_host, parse_ip
from Information_Scan.plugins.InformationGathering.geoip import geoip
from Information_Scan.Requests import Requests
from lib.cli_output import console
from lib.sqldb import Sqldb
from Information_Scan.plugins.PassiveReconnaissance.wappalyzer import WebPage
from Information_Scan.plugins.ActiveReconnaissance.check_waf import checkwaf

def subdomain_save(data):
    Sqldb('result').get_subdomain(data)  #保存到数据库

def web_info(url,flags=1):   #返回H5页面展示信息
    host = parse_host(url)   #整理地址格式得到host  www.baidu.com
    ipaddr = parse_ip(host)   #获得正常的IP,排除DNS服务器
    url = url.strip('/')
    address = geoip(ipaddr)   #获取IP地理位置
    wafresult = checkwaf(url)   #检测waf
    req = Requests()
    try:
        r = req.get(url)    #返回session的长连接
        coding = chardet.detect(r.content).get('encoding')   #获取网站编码格式
        r.encoding = coding
        webinfo = WebPage(r.url, r.text, r.headers).info()    #传入url text headers   返回cms信息 网站标题 服务器
    except Exception:
        webinfo={}

    if webinfo:
        console('Webinfo', host, 'Title: {}\n'.format(webinfo.get('title')))
        console('Webinfo', host, 'Fingerprint: {}\n'.format(webinfo.get('apps')))
        console('Webinfo', host, 'Server: {}\n'.format(webinfo.get('server')))
        console('Webinfo', host, 'WAF: {}\n'.format(wafresult))
    else:
        webinfo = {}
        wafresult = 'None'
    osname = osdetect(host)   #操作系统名称

    data = {
        host: {
            'WAF': wafresult,
            'Ipaddr': ipaddr,
            'Address': address,
            'Webinfo': webinfo,
            'OS': osname,
        }
    }

    if flags == 1:
        return data, webinfo.get('apps'), webinfo.get('title')  #返回目标信息  数据 标题
    else:
        subdomain_save(data)

if __name__ == "__main__":
    web_info('http://127.0.0.1')