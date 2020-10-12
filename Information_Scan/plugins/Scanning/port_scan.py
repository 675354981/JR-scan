import socket
import re
import concurrent.futures
import time
from urllib import parse
from lib.cli_output import console
from lib.sqldb import Sqldb

THREADNUM = 100  # 线程数

def get_server(port):  #获取端口
    SERVER = {
        '21': 'FTP',
        '22': 'SSH',
        '23': 'Telnet',
        '25': 'SMTP',
        '53': 'DNS',
        '68': 'DHCP',
        '8080': 'Proxy',
        '69': 'TFTP',
        '80': 'HTTP',
        '110': 'POP3',
        '135': 'RPC',
        '139': 'NetBIOS',
        '143': 'IMAP',
        '443': 'HTTPS',
        '161': 'SNMP',
        '489': 'LDAP',
        '445': 'SMB',
        '465': 'SMTPS',
        '512': 'Linux R RPE',
        '513': 'Linux R RLT',
        '514': 'Linux R cmd',
        '873': 'Rsync',
        '993': 'IMAPS',
        '1080': 'SSR',
        '1099': 'JavaRMI',
        '1352': 'Lotus',
        '1433': 'MSSQL',
        '1521': 'Oracle',
        '1723': 'PPTP',
        '2082': 'cPanel',
        '2083': 'CPanel',
        '2181': 'Zookeeper',
        '2222': 'DircetAdmin',
        '2375': 'Docker',
        '2604': 'Zebra',
        '3306': 'MySQL',
        '3312': 'Kangle',
        '3389': 'RDP',
        '3690': 'SVN',
        '4440': 'Rundeck',
        '4848': 'GlassFish',
        '5432': 'PostgreSql',
        '5632': 'PcAnywhere',
        '5900': 'VNC',
        '5984': 'CouchDB',
        '6082': 'varnish',
        '6379': 'Redis',
        '9001': 'Weblogic',
        '7778': 'Kloxo',
        '10051': 'Zabbix',
        '8291': 'RouterOS',
        '9300': 'Elasticsearch',
        '11211': 'Memcached',
        '28017': 'MongoDB',
        '50070': 'Hadoop'
    }

    for k, v in SERVER.items():  #遍历端口
        if k == port:
            return v   #返回端口对应名称
    return 'Unknown'


PORTS = [
    21, 22, 23, 25, 26, 37, 47, 49, 53, 69, 70, 79, 80, 81, 82, 83, 84, 88, 89, 110, 111, 119, 123, 129, 135, 137, 139,
    143, 146, 161, 163, 175, 179, 195, 199, 222, 258, 259, 264, 280, 301, 306, 311, 340, 366, 389, 425, 427, 443, 444,
    445, 458, 465, 481, 497, 500, 502, 503, 512, 513, 514, 515, 520, 523, 524, 530, 541, 548, 554, 555, 726, 749, 751,
    765, 771, 777, 783, 787, 789, 808, 843, 873, 880, 888, 898, 901, 902, 981, 987, 990, 992, 993, 995, 996, 999, 1000,
    1007, 1010, 1021, 1023, 1024, 1025, 1080, 1088, 1099, 1102, 1111, 1117, 1119, 1126, 1141, 1325, 1328, 1334, 1352,
    1400, 1417, 1433, 1434, 1443, 1455, 1461, 1471, 1494, 1503, 1515, 1521, 1524, 1533, 2179, 2181, 2196, 2200, 2222,
    2251, 2260, 2288, 2301, 2323, 2332, 2333, 2366, 2375, 2376, 2379, 2399, 2401, 2404, 2433, 2455, 2480, 2492, 2500,
    2522, 2525, 2557, 2601, 2604, 2628, 2638, 2710, 2725, 2800, 2809, 2811, 2869, 2875, 2920, 2998, 3000, 3001, 3003,
    3011, 3013, 3017, 3052, 3071, 3077, 3128, 3168, 3211, 3221, 3260, 3269, 3283, 3299, 3306, 3307, 3310, 3311, 3312,
    3333, 3351, 3367, 3386, 3388, 3389, 3404, 3460, 3476, 3478, 3493, 3517, 3527, 3541, 3542, 3546, 3551, 3560, 3580,
    3659, 3661, 3689, 3690, 3702, 3703, 3737, 3749, 3766, 3780, 3784, 3790, 3794, 3809, 3814, 3851, 3869, 3871, 3878,
    3880, 3889, 3905, 3914, 3918, 3920, 3945, 3971, 3986, 3995, 3998, 4000, 4022, 4040, 4045, 4063, 4064, 4070, 4111,
    4129, 4200, 4224, 4242, 4279, 4321, 4343, 5432, 5550, 5555, 5560, 5566, 5577, 5601, 5631, 5632, 5633, 5666, 5672,
    5683, 5718, 5730, 5800, 5801, 5815, 5822, 5825, 5850, 5858, 5859, 5862, 5877, 5900, 5901, 5915, 5922, 5925, 5938,
    5950, 5952, 5984, 5985, 5986, 6000, 7001, 7002, 7004, 7007, 7019, 7025, 7070, 7071, 7080, 7100, 7103, 7106, 7218,
    7402, 7435, 7443, 7474, 7496, 7512, 7547, 7548, 7549, 7625, 7627, 7657, 7676, 7741, 7777, 7779, 7800, 7903, 7905,
    7911, 8000, 8001, 8008, 8009, 8010, 8031, 8042, 8045, 8060, 8069, 8080, 8081, 8082, 8083, 8086, 8087, 8088, 8089,
    8090, 8091, 8093, 8098, 8099, 8112, 8126, 8139, 8140, 8161, 8181, 8191, 8200, 8222, 8254, 8291, 8300, 8307, 8333,
    8334, 8383, 8390, 8400, 8402, 8433, 8443, 8500, 8554, 8600, 8649, 8654, 8688, 8701, 8800, 8834, 8873, 8880, 8883,
    8888, 8889, 8899, 9151, 9160, 9191, 9200, 9207, 9220, 9290, 9300, 9306, 9415, 9418, 9443, 9485, 9500, 9535, 9575,
    9595, 9600, 9618, 9666, 9869, 9898, 9900, 9903, 9917, 9929, 9943, 9944, 9968, 9981, 9990, 9998, 9999, 10000, 10001,
    10012, 10050, 10051, 10082, 10180, 10215, 10243, 10554, 10566, 10621, 10626, 10778, 11211, 11300, 11967, 12000,
    12124, 12174, 12265, 12345, 12888, 13456, 13579, 13722, 14000, 14003, 14147, 14238, 15000, 15660, 15742, 16010,
    16012, 21571, 22022, 22222, 22939, 23023, 23307, 23389, 23424, 23502, 24212, 24444, 24800, 25105, 25565, 26214,
    27000, 27015, 27016, 27017, 27018, 27019, 27545, 27715, 28015, 28017, 28201, 28561, 30000, 30718, 30951, 31038,
    31337
]

class ScanPort:
    def __init__(self, ipaddr, dbname):   #导入url   数据库名称
        self.ipaddr = ipaddr
        self.dbname = dbname
        self.out = []  #宏定义

    def socket_scan(self, hosts):  #端口信息获取
        ip, port = hosts.split(':')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF_INET，地址要采用ipv4地址类型  SOCK_STREAM:对应tcp  进行连接
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, int(port)))   #socket.connect_ex 返回状态值
            # 建立3次握手成功
            if result == 0:
                try:
                    proto = {"server": get_server(port), "port": port,}
                    self.out.append(proto)
                except:
                    pass

        except Exception as e:
            pass
			
    def save(self, ipaddr, result):
       Sqldb(self.dbname).get_ports(ipaddr, result)   #将信息保存到数据库中

    def run(self, ip):
        hosts = []
        global PORTS, THREADNUM
        for i in PORTS:
            hosts.append('{}:{}'.format(ip, i))
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=THREADNUM) as executor:   #进行处理
                result = {executor.submit(self.socket_scan, i): i for i in hosts}   #端口开放状态  以及端口信息
                for future in concurrent.futures.as_completed(result, timeout=3):
                    future.result()

        except Exception as e:
            pass

    def pool(self):
        out = []
        try:
            # 判断给出的url是www.baiud.com还是www.baidu.com/path这种形式
            if (not parse.urlparse(self.ipaddr).path) and (parse.urlparse(self.ipaddr).path != '/'):   #没有路径而且   最后也不存在/
                self.ipaddr = self.ipaddr.replace('http://', '').replace('https://', '').rstrip('/')   #url切换成完整的url www.baidu.com
            else:
                self.ipaddr = self.ipaddr.replace('http://', '').replace('https://', '').rstrip('/')   #www.baidu.com/programing/virustotal/
                self.ipaddr = re.sub(r'/\w+', '', self.ipaddr)  #www.baidu.com
				
            if re.search(r'\d+\.\d+\.\d+\.\d+', self.ipaddr):   #ip匹配
                ipaddr = self.ipaddr
            else:  
                ipaddr = socket.gethostbyname(self.ipaddr)   # gethostbyname 返回的是 主机名url 的IPv4 的地址格式
            if ':' in ipaddr:
                ipaddr = re.sub(r':\d+', '', ipaddr)  #去掉端口号

            self.run(ipaddr)  #返回端口信息
			
        except Exception as e:
            pass

        self.save(self.ipaddr, self.out)

        for _ in self.out:
            out.append('{}:{}'.format(_.get('server'), _.get('port')))
            console('PortScan', self.ipaddr, '{}:{}\n'.format(_.get('server'), _.get('port')))   #页面展示信息
           
if __name__ == "__main__":
    start_time = time.time()
    ScanPort('127.0.0.1', 'result').pool()
    end_time = time.time()
    print('\nrunning {0:.3f} seconds...'.format(end_time - start_time))

