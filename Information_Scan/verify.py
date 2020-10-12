import re
import hashlib
import random
from Information_Scan.url import parse_host
from Information_Scan.Requests import Requests
from urllib import parse

apps = None
ports = ['CDN:0']
vuln = ['27017', 'Mongodb']


def verify(vuln, port, apps):
    if vuln[0] == 'True':
        return True
    vuln = list(map(lambda x: x.lower(), vuln))
    for i in port:
        server, port = i.split(':')
        if (server in vuln) or (port in vuln):
            return True
    if apps:
        apps = list(map(lambda x: x.lower(), apps))
        for _ in apps:
            if _ in vuln:
                return True
        return False


def get_list(ip, ports):
    result = []
    if ('http:80' in ports and 'http:443' in ports) or ('http:80' in ports and 'https:443' in ports):
        ports.remove('http:80')
    for i in ports:
        server, port = i.split(':')
        server = server.lower()
        ip = parse_host(ip)
        if (server == 'http') and not (server == 'http' and port == '443'):
            url = server + '://' + ip + ':' + port
            if ':80' in url:
                url = re.sub(r':80$', '', url)
            result.append(url)
        if server == 'http' and port == '443':
            url = server + 's://' + ip + ':' + port
            url = re.sub(r':443', '', url)
            result.append(url)
        if server == 'https':
            url = server + '://' + ip + ':' + port
            url = re.sub(r':443$|:80$', '', url)
            result.append(url)

    return list(set(result))


def get_hosts(ip, username):
    result = []
    password = []
    with open('data/password.txt', 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            password.append(i.strip())
    for name in username:
        for passwd in password:
            result.append('{}|{}|{}'.format(ip, name, passwd))
    return result


def verify_https(url):
    # 验证域名是http或者https的
	
    # 如果域名是302跳转 则获取跳转后的地址
    req = Requests()    #发起请求
    url2 = parse.urlparse(url)  #定义了url的标准接口，实现url的各种抽取
    if url2.netloc:   #域名
        url = url2.netloc
    elif url2.path:   #发生跳转    假如跳转的是https://book.qidian.com/
        url = url2.path   #地址
    # noinspection PyBroadException
    try:
        r = req.get('https://' + url)
        getattr(r, 'status_code')   #返回对象的属性
        if r.status_code == 302 or r.status_code == 301:   #发生跳转
            r = req.get('https://' + 'www.' + url)
            if r.status_code == 200:
                return 'https://' + 'www.' + url
        return 'https://' + url   #没发生跳转
    except Exception as e:    #没得用处
        # noinspection PyBroadException
        try:
            req.get('http://' + url)
            return 'http://' + url
        except Exception:
            pass


def get_md5():
    plain = ''.join([random.choice('0123456789') for _ in range(8)])
    md5sum = hashlib.md5()
    md5sum.update(plain.encode('utf-8'))
    md5 = md5sum.hexdigest()
    return [plain, md5]


def verify_ext(apps):  #网站编写语言
    ext = []
    try:
        if 'IIS' in apps or 'Microsoft ASP.NET' in apps or 'ASPX' in apps or 'ASP' in apps:
            ext.extend(['asp', 'aspx'])
        if 'PHP' in apps or 'wamp' in apps or 'phpstudy' in apps or 'Apache' in apps:
            ext.append('php')
        if 'Apache Tomcat' in apps or 'JSP' in apps or 'Jboss' in apps or 'Weblogic' in apps:
            ext.append('jsp')
    except TypeError:
        pass
    ext.extend(['txt', 'xml', 'html'])
    return ext   #返回网站的编写语言