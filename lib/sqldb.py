# coding = utf-8

import sqlite3
import time
import hashlib
import re
from lib.cli_output import console
from Information_Scan.url import parse_host

class Sqldb:    #数据库
    def __init__(self, dbname):
        self.name = dbname #数据库名字
        self.conn = sqlite3.connect(self.name + '.db', check_same_thread=False)   #创建数据库连接

    def commit(self):
        self.conn.commit()     #修改数据库

    def close(self):
        self.conn.close()   #关闭数据库

    def create_webinfo_db(self):
        try:
            cursor = self.conn.cursor()  #创建一个游标对象
            #创建操作系统信息列表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS webinfo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255),
                waf varchar(255) DEFAULT '',
                title varchar(255) DEFAULT '',
                apps varchar(255) DEFAULT '',
                server varchar(255) DEFAULT '',
                address varchar(255) DEFAULT '',
                ipaddr varchar(255) DEFAULT '',
                os varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except sqlite3.OperationalError as e:
            pass

    def create_subdomain_db(self):
        try:
            cursor = self.conn.cursor()  # 创建一个游标对象
            # 创建操作系统信息列表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subdomain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255),
                waf varchar(255) DEFAULT '',
                title varchar(255) DEFAULT '',
                apps varchar(255) DEFAULT '',
                server varchar(255) DEFAULT '',
                address varchar(255) DEFAULT '',
                ipaddr varchar(255) DEFAULT '',
                os varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except sqlite3.OperationalError as e:
            pass

    def create_ports(self):
        try:
            cursor = self.conn.cursor()  #创建一个游标对象
			#创建端口表单
            cursor.execute("""                                       
                CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                ipaddr varchar(255),
                service varchar(255) DEFAULT '',
                port varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except Exception as e:
            pass

    def create_urls(self):
        try: 
            cursor = self.conn.cursor()   #创建一个游标对象
			
			#创建url表单
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255) DEFAULT '',
                url varchar(255) DEFAULT '',
                contype varchar(255) DEFAULT '',
                rsp_code varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except Exception as e:
            pass

    def create_vuln(self):
        try:
            cursor = self.conn.cursor()   #创建游标
			
			#执行命令 创建一个表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vuln (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255),
                vuln varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except:
            pass

    def create_crawl(self):
        try:
            cursor = self.conn.cursor()  #创建游标
			
            #执行命令 创建一个表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Crawl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time varchar(255),
                domain varchar(255),
                type varchar(255) DEFAULT '',
                leaks varchar(255) DEFAULT '',
                md5 varchar(40) UNIQUE
                )
                """)
        except Exception as e:
            pass

    def insert_subdomain(self, query, values):
        try:
            cursor = self.conn.cursor()   #创建游标
            cursor.execute(query, values)   #命令执行 添加数据到表里面
            self.commit()   #关闭数据库
        except Exception as e:
            pass

    def insert_webinfo(self, query, values):
        try:
            cursor = self.conn.cursor()   #创建游标
            cursor.execute(query, values)   #命令执行 添加数据到表里面
            self.commit()   #关闭数据库
        except Exception as e:
            pass

    def insert_ports(self, query, values):  #格式 具体内容
        try:
            cursor = self.conn.cursor()  #制定游标
            cursor.execute(query, values)   #命令执行 添加数据到表里面
            self.commit()  #事物提交命令 
        except Exception as e:
            pass

    def insert_urls(self, query, values):
        try:
            cursor = self.conn.cursor()  #制定游标
            cursor.execute(query, values)   #命令执行 添加数据到表里面
        except Exception as e:
            pass

    def insert_vuln(self, query, values):
        try:
            cursor = self.conn.cursor()  #制定游标
            cursor.execute(query, values)     #命令执行 添加数据到表里面
        except Exception as e:
            pass

    def insert_crawl(self, query, values):
        try: 
            cursor = self.conn.cursor()  #制定游标
            cursor.execute(query, values)  #命令执行 添加数据到表里面
            self.commit()
        except Exception as e:
            pass

    def get_urls(self, urls):
        self.create_urls()  #创建列表
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #显示开始时间
        for url in urls:   #遍历网站数据
            for k, v in url.items():
                url=v.get('url')
                contype=v.get('contype')
                rsp_code=v.get('rsp_code')
                md5sum = hashlib.md5()  #定义md5格式
                strings = str(k) + str(url)   #添加信息
                md5sum.update(strings.encode('utf-8'))  #计算md5值
                md5 = md5sum.hexdigest()   #返回加密后的md5的值
                values = (timestamp, k,url,contype,rsp_code, md5)
                query = "INSERT OR IGNORE INTO urls (time, domain, url, contype,rsp_code,md5) VALUES (?,?,?,?,?,?)"
                self.insert_urls(query, values)   #命令执行
        self.commit()
        self.close()

    def get_ports(self, ipaddr, ports):
        self.create_ports()  #创建对应的数据库中的表
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  #显示开始时间
        for i in ports:
            service = i.get('server')
            port = i.get('port')
            md5sum = hashlib.md5()  #定义md5格式
            strings = str(ipaddr) + str(service) + str(port)   #字段信息
            md5sum.update(strings.encode('utf-8'))  #计算md5值
            md5 = md5sum.hexdigest()   #返回加密后的md5的值
            values = (timestamp, ipaddr, service, port, md5)
            query = "INSERT OR IGNORE INTO ports (time, ipaddr, service, port,md5) VALUES (?,?,?,?,?)"
            self.insert_ports(query, values)   #命令执行

    def get_vuln(self, domain, vuln):  #ip 结果    脚本攻击数据
        self.create_vuln()  #创建一个表
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #标记开始时间
        md5sum = hashlib.md5()  #创建hashlib的md5对象
        strings = str(domain)
        md5sum.update(strings.encode('utf-8'))   #将字符串载入到md5对象中，获得md5算法加密。
        md5 = md5sum.hexdigest()    #通过hexdigest()方法，获得new_md5对象的16进制md5显示。
        values = (timestamp, domain, vuln, md5)
        query = "INSERT OR IGNORE INTO vuln (time, domain, vuln, md5) VALUES (?,?,?,?)"
        self.insert_vuln(query, values)  #命令执行
        self.commit()  #事务提交
        self.close()  #关闭

    def get_crawl(self, domain, crawl):
        self.create_crawl()  #创建表单
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  #设定开始时间
        for i in crawl:   #遍历信息
            if 'Dynamic:' in i:
                type = 'Dynamic link'
            else:
                type = 'Leaks'
            md5sum = hashlib.md5()   #创建hashlib的md5对象
            try:
                text = re.search(r'(?<=Email: ).*|(?<=Phone: ).*', i).group()  #进行正则匹配
            except:
                text = str(i)
            strings = str(domain) + text
            md5sum.update(strings.encode('utf-8'))  #将字符串载入到md5对象中，获得md5算法加密。
            md5 = md5sum.hexdigest()   #通过hexdigest()方法，获得new_md5对象的16进制md5显示。
            values = (timestamp, domain, type, i, md5)
            query = "INSERT OR IGNORE INTO Crawl (time, domain, type, leaks, md5) VALUES (?,?,?,?,?)"
            self.insert_crawl(query, values)   #命令执行
        self.commit()
        self.close()

    def get_subdomain(self, webinfo):  # 保存到数据库
        self.create_subdomain_db()  # 创建数据库列表
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 设定开始时间

        for k, v in webinfo.items():  # 操作系统的各种信息
            apps = v.get('Webinfo').get('apps')  # 获得其中的app信息
            if apps:
                apps = ' , '.join(apps)
            else:
                apps = None

            waf = v.get('WAF')
            if waf == 'None':
                waf = None

            title = v.get('Webinfo').get('title')
            if not title:
                title = None

            address = v.get('Address')
            if address == 'None' or not address:
                address = None

            server = v.get('Webinfo').get('server')
            if server == 'None' or not server:
                server = None

            os = v.get('OS')
            if not os or os == 'None':
                os = None

            ipaddr = v.get('Ipaddr')
            if not ipaddr or ipaddr == 'None':
                ipaddr = None

            md5sum = hashlib.md5()  # 创建hashlib的md5对象
            strings = str(k) + str(title) + str(server)
            md5sum.update(strings.encode('utf-8'))  # 将字符串载入到md5对象中，获得md5算法加密。
            md5 = md5sum.hexdigest()  # 通过hexdigest()方法，获得new_md5对象的16进制md5显示。
            values = (timestamp, k, waf, title, apps, server, address, ipaddr, os, md5)
            query = "INSERT OR IGNORE INTO subdomain (time, domain, waf, title, apps, server, address, ipaddr, os, md5) VALUES (?,?,?,?,?,?,?,?,?,?)"
            self.insert_subdomain(query, values)  # 命令执行
        self.commit()
        self.close()

    def get_webinfo(self, webinfo):   #保存到数据库
        self.create_webinfo_db()  #创建数据库列表
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #设定开始时间

        for k, v in webinfo.items():   #操作系统的各种信息
            apps = v.get('Webinfo').get('apps')   #获得其中的app信息
            if apps:
                apps = ' , '.join(apps)
            else:
                apps = None

            waf = v.get('WAF')
            if waf == 'None':
                waf = None

            title = v.get('Webinfo').get('title')
            if not title:
                title = None
				
            address = v.get('Address')
            if address == 'None' or not address:
                address = None
				
            server = v.get('Webinfo').get('server')
            if server == 'None' or not server:
                server = None
				
            os = v.get('OS')
            if not os or os == 'None':
                os = None
				
            ipaddr = v.get('Ipaddr')
            if not ipaddr or ipaddr == 'None':
                ipaddr = None
				
            md5sum = hashlib.md5() #创建hashlib的md5对象
            strings = str(k) + str(title) + str(server)
            md5sum.update(strings.encode('utf-8'))  #将字符串载入到md5对象中，获得md5算法加密。
            md5 = md5sum.hexdigest()   #通过hexdigest()方法，获得new_md5对象的16进制md5显示。
            values = (timestamp, k, waf, title, apps, server, address, ipaddr, os,md5)
            query = "INSERT OR IGNORE INTO webinfo (time, domain, waf, title, apps, server, address, ipaddr, os, md5) VALUES (?,?,?,?,?,?,?,?,?,?)"
            self.insert_webinfo(query, values)   #命令执行
        self.commit()
        self.close()

    def query_db(self, hosts):   #写入到数据库，返回成功的目标
        result = []
        error = False
        for i in hosts:
            try:
                domain = parse_host(i)   #获得主机host头
                cursor = self.conn.cursor()   #创建数据库游标
                sql = "select 1 from webinfo where domain = '{}' limit 1".format(domain)
                cursor.execute(sql)    #执行sql语句
                values = cursor.fetchall()  #获取结果集   内容形成一个列
                if not values:
                    result.append(i)    #没有目标添加到result里
                else:
                    console('CheckDB', i, 'In the db file\n')    #结果展示
            except sqlite3.OperationalError:
                return hosts
        self.commit()    #提交修改请求
        self.close()   #关闭数据库
        if error:
            return hosts
        else:
            return result     #返回成功的目标

    def query(self, sql):   #执行命令
        try:
            cursor = self.conn.cursor()  #创建数据库游标
            cursor.execute(sql)  #执行命令
            values = cursor.fetchall()   #使用fetchall() 方法获取多条数据。
            return values
        except sqlite3.OperationalError:
            pass
        finally:
            self.commit()   # 提交修改请求
            self.close()  #关闭


