import ipaddress    #处理IPv4和IPv6地址的
import re
from lib.active import ActiveCheck

def add(target):
    try:
        if re.search(r'\.txt$',target):
            hosts = read_file(target)
            if hosts:
                return hosts
            else:
                return []

        if re.search(r'(\.\d+\/\d+$)', target):
            hosts=inet(target)
            if hosts:
                return hosts
            else:
                return []

        else:
            if ActiveCheck([target]).pool():
                return [target]
            else:
                return []
    except:
        pass
            
def read_file(file):  #文件
    hosts = []
    try:
        with open(file, 'rt') as f:
            for ip in f.readlines():
                hosts.append(ip.strip())   #保存到host列中
        hosts2 = ActiveCheck(hosts).pool()   #对不存在的IP进行测试
        return hosts2
    except FileNotFoundError:
        print('input file')

def inet(net):   #C段
    hosts = []
    try:
        result = list(ipaddress.ip_network(net))    #将C段切为一个个单独IP，写入列中
        for ip in result:
            hosts.append(str(ip))
    except Exception as e:
        print("The task could not be carried out. {}".format(str(e)))
    hosts2 = ActiveCheck(hosts).pool()
    return hosts2



