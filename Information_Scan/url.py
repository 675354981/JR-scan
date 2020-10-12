from urllib import parse
import re
import dns.resolver


def parse_host(url):   #整理主机头
    # 根据url得到主机host 例如 http://www.baidu.com:80 返回 www.baidu.com
    if (not parse.urlparse(url).path) and (parse.urlparse(url).path != '/'):
        host = url.replace('http://', '').replace('https://', '').rstrip('/')
    else:
        host = url.replace('http://', '').replace('https://', '').rstrip('/')   #删除http https
        host = re.sub(r'/\w+', '', host)  #删除域名之外的东西
    if ':' in host:
        host = re.sub(r':\d+', '', host)   #删除端口
    return host


def parse_ip(host):     #获得正常的IP,
    host = parse_host(host)      #获得主机头  www.baidu.com
    # 根据domain得到ip 例如www.xxx.com 得到 x.x.x.x
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1', '8.8.8.8']
		
        a = resolver.query(host, 'A')   #查询类型为A记录
        for i in a.response.answer:     #检测是不是特殊的IP
            for j in i.items:
                if hasattr(j, 'address'):
                    if not re.search(r'1\.1\.1\.1|8\.8\.8\.8|127\.0\.0\.1|114\.114\.114\.114|0\.0\.0\.0', j.address):
                        return j.address
    except Exception as e:
        pass
    return host    #返回正常的IP


