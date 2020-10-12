import concurrent.futures
import subprocess
import re
import xml
import platform  # 获取操作系统的相关信息
import time
import nmap  # nmap模块
import dns.resolver
from urllib import parse  # parse模块的作用：url的解析，合并，编码，解码
from lib.cli_output import console
from lib.setting import PING

class ActiveCheck:
    def __init__(self, hosts):
        self.hosts = hosts
        self.out = []

    def check(self, url):  # 检测导入的IP
        loc = parse.urlparse(url)  # urlparse()实现URL的识别和分段
        if getattr(loc, 'netloc'):  # getattr() 函数用于返回一个对象属性值。
            host = loc.netloc  # 获得Ip域名
        else:
            host = loc.path  # 获得Ip路径

        try:
            # 判断是IP还是域名，域名的话需要检测域名解析
            if not re.search(r'\d+\.\d+\.\d+\.\d+', host):
                # 验证DNS存活并且DNS解析不能是一些特殊IP（DNSIP、内网IP）
                # resolver = dns.resolver.Resolver()
                # resolver.nameservers = ['1.1.1.1', '8.8.8.8']
                a = dns.resolver.query(host, 'A')  # 查询类型为A记录
                for i in a.response.answer:  # 通过response.answer获取查询回应信息
                    for j in i.items:
                        if hasattr(j, 'address'):  # 用于判断对象是否包含对应的属性。
                            if re.search(r'1\.1\.1\.1|8\.8\.8\.8|127\.0\.0\.1|114\.114\.114\.114|0\.0\.0\.0',
                                         j.address):
                                return False
            if PING:
                try:
                    # Windows调用ping判断存活 Linux调用nmap来判断主机存活
                    # nmap判断存活会先进行ping然后连接80端口，这样不会漏掉
                    if platform.system() == 'Windows':  # 获得系统名称
                        subprocess.check_output(['ping', '-n', '2', '-w', '1', host])  # 执行命令
                        self.out.append(url)  # 添加url到列
                    else:
                        nm = nmap.PortScanner()  # 实例化
                        result = nm.scan(hosts=host, arguments='-sP -n')  # 可选参数，要扫描的方式
                        for k, v in result.get('scan').items():
                            if not v.get('status').get('state') == 'up':  # 获得主机信息
                                console('PING', host, "is not alive\n")  # 结果展示
                                return False
                            else:
                                self.out.append(url)  # 添加url到列
                except:
                    console('PING', host, "is not alive\n")  # 结果展示
                    return False
            else:
                self.out.append(url)

        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            console('DnsCheck', host, "No A record\n")  # 描述失败原因
        except dns.exception.Timeout:
            console('DnsCheck', host, "Timeout\n")

    def pool(self):  # 数据处理模块
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:  # 被用来创建线程池代码
                result = {executor.submit(self.check, i): i for i in self.hosts}  # 异步提交IP
                for future in concurrent.futures.as_completed(result, timeout=3):  # 返回一个包含 result 所指定的 Future 实例
                    future.result()
        except:
            pass
        return self.out  # 返回存活的主机

if __name__ == "__main__":
    start_time = time.time()
    active_hosts = ActiveCheck(['127.0.0.1']).pool()
    end_time = time.time()
    print(active_hosts)
    print('\nrunning {0:.3f} seconds...'.format(end_time - start_time))
