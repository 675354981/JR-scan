import sys
import re
import gevent
import platform
if sys.version > '3':
    from queue import Queue
else:
    from Queue import Queue
import os
import dns.resolver
from IPy import IP
import gevent
from lib.cli_output import console
from Information_Scan.web_info import web_info
from lib.setting import *
from gevent import monkey
monkey.patch_all()

class sub_domain(object):
    def __init__(self, idomain):
        if re.search(r'\.org\.cn|\.com\.cn|\.gov\.cn|\.edu\.cn|\.mil|\.aero|\.int|\.go\.\w+$|\.ac\.\w+$', idomain):
            self.target_domain = idomain.split(".", 1)[-1]                     # adbc.com.cn
        else:
            self.target_domain = idomain.split(".", idomain.count(".") - 1)[-1]  # baidu.com

        self.level = 2
        self.all_task = Queue()
        self.sub_dict = sub_dict
        self.next_sub_dict = next_sub_dict
        self.cnd_dict = cnd_dict
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [
            '114.114.114.114',
            '114.114.115.115',
            '223.5.5.5',
            '223.6.6.6',
            '180.76.76.76',
            '119.29.29.29',
            '182.254.116.116',
            '210.2.4.8',
            '112.124.47.27',
            '114.215.126.16',
            '101.226.4.6',
            '218.30.118.6',
            '123.125.81.6',
            '140.207.198.6'
            '8.8.8.8',
            '8.8.4.4']
        self.resolver.timeout = 10

        self.add_ulimit()
        self.queues = Queue()
        self.dict_cname = dict()
        self.dict_ip = dict()
        self.dict_ip_block = dict()
        self.ip_flag = dict()
        self.cdn_set = set()
        self.queue_sub = Queue()
        self.active_ip_dict = dict()
        self.dict_ip_count = dict()
        self.found_count = 0

        self.set_next_sub = self.load_next_sub_dict()
        self.set_cdn = self.load_cdn()
        self.load_sub_dict_to_queue()
        self.segment_num = 5000

    def add_ulimit(self):
        if (platform.system() != "Windows"):
            os.system("ulimit -n 65535")

    def load_cdn(self):
        cdn_set = set()
        with open(self.cnd_dict, 'r') as file_cdn:
            for cdn in file_cdn:
                cdn_set.add(cdn.strip())
        return cdn_set

    def load_next_sub_dict(self):
        next_sub_set = set()
        with open(self.next_sub_dict, 'r') as file_next_sub:
            for next_sub in file_next_sub:
                next_sub_set.add(next_sub)
        return next_sub_set

    def load_sub_dict_to_queue(self):
        with open(self.sub_dict, 'r') as file_sub:
            for sub in file_sub:
                domain = "{sub}.{target_domain}".format(
                    sub=sub.strip(), target_domain=self.target_domain)
                self.queues.put(domain)

    def check_cdn(self, cname):
        for cdn in self.set_cdn:
            if (cdn in cname or 'cdn' in cname):
                return True
            self.cdn_set.add(cname)
        return False

    def get_type_id(self, name):
        return dns.rdatatype.from_text(name)

    def query_domain(self, domain):
        list_ip, list_cname = [], []
        try:
            record = self.resolver.query(domain)
            for A_CNAME in record.response.answer:
                for item in A_CNAME.items:
                    if item.rdtype == self.get_type_id('A'):
                        list_ip.append(str(item))
                        self.dict_ip_block[domain] = list_ip
                    elif (item.rdtype == self.get_type_id('CNAME')):
                        list_cname.append(str(item))
                        self.dict_cname[domain] = list_cname
                    elif (item.rdtype == self.get_type_id('TXT')):
                        pass
                    elif item.rdtype == self.get_type_id('MX'):
                        pass
                    elif item.rdtype == self.get_type_id('NS'):
                        pass
        except Exception as e:
            pass

    def get_block(self):
        domain_list = list()
        if (self.queues.qsize() > self.segment_num):
            for num in range(self.segment_num):
                domain_list.append(self.queues.get())
        else:
            for num in range(self.queues.qsize()):
                domain_list.append(self.queues.get())
        return domain_list

    def deweighting_subdomain(self):
        temp_list = list()
        for subdomain, ip_list in self.dict_ip_block.items():
            ip_str = str(sorted(ip_list))
            if (self.dict_ip_count.__contains__(ip_str)):
                if (self.dict_ip_count[ip_str] > 30):
                    temp_list.append(subdomain)
                else:
                    self.dict_ip_count[ip_str] = self.dict_ip_count[ip_str] + 1
            else:
                self.dict_ip_count[ip_str] = 1

            for filter_ip in [ '222.221.5.253','222.221.5.252','1.1.1.1']:
                if (filter_ip in ip_str):
                    temp_list.append(subdomain)

        for subdomain in temp_list:
            try:
                del self.dict_ip_block[subdomain]
                del self.dict_cname[subdomain]
            except Exception:
                pass

        self.dict_ip.update(self.dict_ip_block)
        self.found_count = self.dict_ip.__len__()

        for subdomain, ip_list in self.dict_ip_block.items():
            if (str(subdomain).count(".") < self.level):
                self.queue_sub.put(str(subdomain))

        self.dict_ip_block.clear()

    def handle_data(self):
        for subdomain, cname_list in self.dict_cname.items():
            for cname in cname_list:
                if (self.check_cdn(cname)):
                    self.dict_cname[subdomain] = "Yes"
                else:
                    self.dict_cname[subdomain] = "No"
        for subdomain, ip_list in self.dict_ip_block.items():
            for ip in ip_list:
                if (IP(ip).iptype() == 'PRIVATE'):
                    self.dict_ip[subdomain] = "private({ip})".format(ip=ip)
                else:
                    try:
                        key_yes = self.dict_cname[subdomain]
                    except KeyError:
                        key_yes = "No"
                    if (key_yes == "No"):
                        CIP = (IP(ip).make_net("255.255.255.0"))
                        if CIP in self.ip_flag:
                            self.ip_flag[CIP] = self.ip_flag[CIP] + 1
                        else:
                            self.ip_flag[CIP] = 1

                        if CIP in self.active_ip_dict:
                            active_ip_list = self.active_ip_dict[CIP]
                            if (ip not in active_ip_list):
                                active_ip_list.append(ip)
                                self.active_ip_dict[CIP] = active_ip_list
                        else:
                            active_ip_list = []
                            active_ip_list.append(ip)
                            self.active_ip_dict[CIP] = active_ip_list

    def worker(self):
        current_payload = self.all_task.get()
        try:
            console('sub_domain', self.target_domain, current_payload + '\n')
            web_info(current_payload, flags=2)
        except :
            pass

    def execution(self):
        i = 0
        while not self.queues.empty():
            i = i + 1
            domain_list = self.get_block()   #pin jie
            coroutines = [gevent.spawn(self.query_domain, l)
                          for l in domain_list]
            try:
                gevent.joinall(coroutines)
            except KeyboardInterrupt:
                print('user stop')
                sys.exit(1)

            self.deweighting_subdomain()

        self.handle_data()

        for subdomain, ip_list in self.dict_ip.items():
            self.all_task.put(subdomain)

        try:
            while not self.all_task.empty():
                all_task = [gevent.spawn(self.worker) for i in range(30)]
                gevent.joinall(all_task)
        except:
            pass

            # console('sub_domain', self.target_domain, subdomain + '\n')  # 旁站进行展示
            # web_info(subdomain,flags=2)  # 返回目标信息 数据 网站标题

if __name__ == '__main__':
    brute = sub_domain('4399.com')
    try:
        brute.execution()
    except KeyboardInterrupt:
        print('user stop')