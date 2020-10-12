import json
import re
import time
from lib.sqldb import Sqldb
from lib.cli_output import console

dbname = 'result'

def get_port(ipaddr):  #获得Ip端口
    try:
        sql = "select port from ports where ipaddr='{}'".format(ipaddr)   #命令
        getport = Sqldb(dbname).query(sql)  #命令执行
        if getport:
            result = []
            for i in getport:   #遍历端口
                result.append(i[0])
            result = list(map(int, result))  #强制转换
            result = sorted(result)
            result = list(map(str, result))
            ports = ' , '.join(result)   
            return ports   #元组
    except Exception as e:
        pass


def gen_subdomain():
    tableData = []
    sql = 'select time,domain,waf,title,apps,server,address,ipaddr,os from subdomain'
    try:
        res = Sqldb(dbname).query(sql)
        for i in res:
            time, domain, waf, title, apps, server, address, ipaddr, os = i

            webinfo = {
                "time": time,
                "domain": domain,
                "waf": waf,
                "title": title,
                "apps": apps,
                "server": server,
                "address": address,
                "ipaddr": ipaddr,
                "os": os,
            }
            tableData.append(webinfo)  # 网站信息添加到列表

        column = [
            {
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "domain",
                "title": "domain",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "waf",
                "title": "waf",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "title",
                "title": "title",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "apps",
                "title": "apps",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "server",
                "title": "server",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "address",
                "title": "address",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "ipaddr",
                "title": "ipaddr",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "os",
                "title": "os",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
        ]

        data = {"name": "Subdomain", "tableData": tableData, "columns": column}  # 字典格式写进网站
        return data
    except TypeError:
        pass
    except Exception as e:
        pass

def gen_webinfo():
    tableData = []
    sql = 'select time,domain,waf,title,apps,server,address,ipaddr,os from webinfo'   #命令
    try:
        res = Sqldb(dbname).query(sql)   #命令执行
        for i in res:
            time, domain, waf, title, apps, server, address, ipaddr, os = i
            ports = get_port(domain)  #Ip端口列表
			
            webinfo = {
                "time": time,
                "domain": domain,
                "waf": waf,
                "title": title,
                "apps": apps,
                "server": server,
                "address": address,
                "ipaddr": ipaddr,
                "ports": ports,
                "os": os,
            }
            tableData.append(webinfo)  #网站信息添加到列表
			
        column = [
            {
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "domain",
                "title": "domain",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "waf",
                "title": "waf",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "title",
                "title": "title",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "apps",
                "title": "apps",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "server",
                "title": "server",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "address",
                "title": "address",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "ipaddr",
                "title": "ipaddr",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "ports",
                "title": "ports",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "os",
                "title": "os",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
        ]
		
        data = {"name": "webinfo", "tableData": tableData, "columns": column}   #字典格式写进网站
        return data
    except TypeError:
        pass
    except Exception as e:
        pass


def gen_ports():
    tableData = []
    sql = 'select time,ipaddr,service,port from ports'  #命令
    try:
        res = Sqldb(dbname).query(sql)   #命令执行
        for i in res:
            time, ipaddr, service, port = i
            ports = {"time": time, "ip": ipaddr, "port": port, "service": service,}   #端口信息
            tableData.append(ports)  #信息添加到列表
        column = [
            {
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "ip",
                "title": "IP",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "port",
                "title": "PORT",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "service",
                "title": "SERVICE",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
           
        ]
		
        data = {"name": "Ports", "tableData": tableData, "columns": column}
        return data   #返回信息
    except TypeError:
        pass
    except Exception as e:
        pass


def gen_urls():
    tableData = []
    sql = 'select time,domain,url,contype,rsp_code from urls'  #命令
    try:
        res = Sqldb(dbname).query(sql)  #命令执行
        if res:
            for i in res:
                time, domain, url, contype, rsp_code = i
                urls = {
                    "time": time,
                    "domain": domain,
                    "url": url,
                    "contype": contype,
                    "rsp_code": rsp_code
                }
                tableData.append(urls)   #添加
            column = [{
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            }, {
                "field": "domain",
                "title": "Domain",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            }, {
                "field": "url",
                "title": "URL",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            }, {
                "field": "contype",
                "title": "ConType",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },  {
                "field": "rsp_code",
                "title": "rsp_code",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            }]
            data = {"name": "URLS", "tableData": tableData, "columns": column}
            return data  #信息返回
    except TypeError:
        pass
    except Exception as e:
        pass


def gen_vuln():
    tableData = []
    sql = 'select time, domain, vuln from vuln'
    try:
        res = Sqldb(dbname).query(sql)
        for i in res:
            time, ip, vuln = i
            vuln = {"time": time, "ip": ip, "vuln": vuln}
            tableData.append(vuln)
        column = [
            {
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "ip",
                "title": "IP",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "vuln",
                "title": "VULN",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
        ]
        data = {"name": "Vuln", "tableData": tableData, "columns": column}
        return data
    except TypeError:
        pass
    except Exception as e:
        pass


def gen_crawl():
    tableData = []
    sql = 'select time, domain, type,leaks from crawl'  #命令
    try:
        res = Sqldb(dbname).query(sql)   #命令执行
        for i in res:
            time, domain, type, leaks = i
            vuln = {"time": time, "domain": domain, "type": type, "leaks": leaks}
            tableData.append(vuln)   #添加到列表
        column = [
            {
                "field": "time",
                "title": "TIME",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "domain",
                "title": "DOMAIN",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "type",
                "title": "TYPE",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
            {
                "field": "leaks",
                "title": "Leaks",
                "width": 100,
                "tilteAlign": "center",
                "columnAlign": "center"
            },
        ]
        data = {"name": "Crawl", "tableData": tableData, "columns": column}
        return data
    except TypeError:
        pass
    except Exception as e:
        pass

def gener():   
    out = []
    for i in [gen_webinfo(), gen_urls(), gen_ports(), gen_vuln(), gen_crawl(),gen_subdomain()]:
        if i:
            out.append(i)
    result = {"table": out}
    result = json.dumps(result)   #将dict类型的数据转成str
    result = re.sub(r'^{|}$', '', result)   #格式整理
    times = time.strftime("%Y%m%d%H%M%S", time.localtime())   #设定开始时间
    name = 'scan_' + times + '.html'
    with open('report/report.htm', 'r', encoding='utf-8') as f, open(name, 'w') as f1:
        text = f.read()
        console('H5_Create',name,'创建......\n')
        time.sleep(2)
        f1.write(text.replace("'summary': {}", result))  #H5页面展示

if __name__ == "__main__":
    gener()


