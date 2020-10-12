import requests
import urllib3
import hashlib
import random
import re
import ssl
import socks
import socket
from Information_Scan.random_header import get_ua
from lib.setting import TIMEOUT, COOKIE, SOCKS5

def verify(url):   #判断是不是https  并返回携带协议的url
    if not re.search('http:|https:', url):
        url = 'http://' + url
    return url


class Requests:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   #忽略警告  HTTPS请求不支持证书验证
        requests.packages.urllib3.disable_warnings()   #忽略警告

        self.timeout = TIMEOUT   #延迟
        self.session = requests.Session()  #下次请求自动带上请求参数
        self.headers = get_ua()   #自定义请求头

        if COOKIE == 'random':
            plain = ''.join([random.choice('0123456789') for _ in range(8)])  #随机选8个  37247698
            md5sum = hashlib.md5()  #创建hashlib的md5对象
            md5sum.update(plain.encode('utf-8'))   #将字符串载入到md5对象中，获得md5算法加密。
            md5 = md5sum.hexdigest()   #通过hexdigest()方法，获得new_md5对象的16进制md5显示。
            self.headers.update({'Cookie': 'SESSION=' + md5})  #更新headers头信息
        else:
            self.headers.update(COOKIE)  #更新headers头信息

        if SOCKS5:   #代理
            ip, port = SOCKS5
            socks.set_default_proxy(socks.SOCKS5, ip, port)
            socket.socket = socks.socksocket  #建立连接

    def scan(self, url):
        url = verify(url)  #https://www.baidu.com  http://www.baidu.com
        try:
            r = self.session.get(url,
                                 timeout=self.timeout,
                                 headers=self.headers,
                                 verify=False,  #证书
                                 stream=True,
                                 allow_redirects=False)   #重定向
            return r   #连接信息

        except:
            pass


    def get(self, url):
        url = verify(url)   #判断是不是https
        try:
            r = self.session.get(url, timeout=self.timeout, headers=self.headers, verify=False, allow_redirects=False)  #长连接
            return r    #返回长连接信息
        except:
            pass


    def post(self, url, data):
        url = verify(url)   #https://www.baidu.com
        try:
            r = self.session.post(url,
                                  data=data,
                                  timeout=self.timeout,
                                  headers=self.headers,
                                  verify=False,
                                  allow_redirects=False)   #allow_redirects=False  不准重定向
            return r
        except:
            pass

    def request(self, url, method, data=None, headers=None):    #发起请求
        url = verify(url)    #http|https分析后的url
        try:
            if method == 'get':
                r = self.session.get(url, timeout=self.timeout, headers=headers, verify=False, allow_redirects=True)  #verify处理不信任的证书
                return r
            else:
                r = self.session.post(url,
                                      data=data,
                                      timeout=self.timeout,
                                      headers=headers,
                                      verify=False,
                                      allow_redirects=False)   
                return r
        except:
            pass

