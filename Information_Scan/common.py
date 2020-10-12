from Information_Scan.web_info import web_info
from lib.sqldb import Sqldb
from Information_Scan.verify import verify_https
from Information_Scan.plugins.Scanning.port_scan import ScanPort
from Information_Scan.plugins.Scanning.async_scan import DirScan
from Information_Scan.plugins.PassiveReconnaissance.sub_domain import sub_domain
from Information_Scan.url import parse_host

def web_save(webinfo, dbname):
    Sqldb(dbname).get_webinfo(webinfo)  #保存到数据库

def start(target, dbname):
    title = 'test'
    url = verify_https(target)  #判断是否跳转并获得最终url http+url还是https+url

    data, apps, title = web_info(url)  #返回目标信息 数据 网站标题

    host = parse_host(url)
    subip = sub_domain(host).execution()  # 子域名查询

    open_port = ScanPort(url, dbname)   #端口信息
    open_port.pool()

    dirscan = DirScan(dbname, url)   #实例化
    dirscan.pool()   #网站信息探测，保存到数据库

    web_save(data, dbname)  #操作系统各种信息  数据库名字

if __name__ == "__main__":
    start('http://127.0.0.1')