import gevent
from gevent import monkey
monkey.patch_all()
from Information_Scan.plugins.Scanning.check_target import Inspector
import hashlib
import urllib
import requests
from gevent.queue import Queue
from lxml import etree
from lib.cli_output import console
from lib.sqldb import Sqldb
from Information_Scan.random_header import get_ua
from lib.setting import *

requests.packages.urllib3.disable_warnings()

class DirScan():
    def __init__(self,dbname,url):
        self.thread_num=30   #扫描线程
        self.url=url
        self.autodiscriminator_md5 = set()
        self.crawl_mode_dynamic_fuzz_temp_dict=set()
        self.similar_urls_set=set()  #相似的目录合集
        self.crawl_mode_dynamic_fuzz_dict = list()
        self.outjson = []
        # 创建all_tasks队列
        self.all_task = Queue()
        self.dbname = dbname
        self.headers = get_ua()
        self.dir = dir
    def urlSimilarCheck(self,url):
        '''
        @description: url相似度分析，当url路径和参数键值类似时，则判为重复
        @param {type}
        @return: 非重复返回True
        '''
        url_struct = urllib.parse.urlparse(url)
        query_key = '|'.join(sorted([i.split('=')[0] for i in url_struct.query.split('&')]))
        url_hash = hash(url_struct.path + query_key)
        if url_hash not in self.similar_urls_set:
            self.similar_urls_set.add(url_hash)
            return True
        return False

    def scanModeHandler(self,url):
        '''
        @description: 扫描模式处理，加载payloads
        @param {type}
        @return:
        '''
        payloadlists = []

       #目录扫描模式
        if dict_mode:  #添加字典
            with open(self.dir, 'r', encoding='utf-8') as f:
                for i in f.readlines():
                    payloadlists.append(i.strip())  # 形成路径 每行进行切换

        #递归爬取模式
        if crawl_mode:
            #自定义header
            headers = self.headers
            try:
                response = requests.get(url, headers=headers, timeout=3, verify=False, allow_redirects=False,)
                #获取页面url
                if (response.status_code in [200,]) and response.text:
                    html = etree.HTML(response.text)
                    #加载自定义xpath用于解析html
                    urls = html.xpath(crawl_mode_parse_html)
                    for url in urls:
                        #去除相似url
                        if self.urlSimilarCheck(url):
                            #判断:1.是否同域名 2.netloc是否为空(值空时为同域)。若满足1或2，则添加到temp payload
                            if (urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(self.url).netloc) or urllib.parse.urlparse(url).netloc == '':
                                self.crawl_mode_dynamic_fuzz_temp_dict.add(url)
                self.crawl_mode_dynamic_fuzz_temp_dict = self.crawl_mode_dynamic_fuzz_temp_dict - {'#', ''}

                for i in self.crawl_mode_dynamic_fuzz_temp_dict:
                    self.crawl_mode_dynamic_fuzz_dict.append(urllib.parse.urlparse(i).path)

                payloadlists.extend(set(self.crawl_mode_dynamic_fuzz_dict))

            except:
                pass

        return payloadlists

    def intToSize(self,bytes):
        '''
        @description: bits大小转换，对人类友好
        @param {type}
        @return:
        '''
        b = 1024 * 1024 * 1024 * 1024
        a = ['t', 'g', 'm', 'k', '']
        for i in a:
            if bytes >= b:
                return '%.2f%sb' % (float(bytes) / float(b), i)
            b /= 1024
        return '0b'

    def responseHandler(self,response):
        '''
        @description: 处理响应结果
        @param {type}
        @return:
        '''
        # 结果处理阶段
        try:
            size = self.intToSize(int(response.headers['content-length']))
        except (KeyError, ValueError):
            size = self.intToSize(len(response.content))
        # 跳过大小为skip_size的页面
        if size == "None":
            return
        #与404页面进行匹配
        if hashlib.md5(response.content).hexdigest() in self.autodiscriminator_md5:
            return

        # 自定义状态码显示
        if response.status_code in [200,]:
            msg = response.url
            host2 = self.url.replace('http://', '').replace('https://', '').rstrip('/')
            console('URLS', host2, msg + '\n')  # 目标展示
            data = {
                host2: {
                    "rsp_code": str(response.status_code),
                    "contype": response.headers.get('content-type'),
                    "url": msg
                }
            }
            self.outjson.append(data)

    def worker(self):
        '''
        @description: 封包发包穷举器
        @param {type}
        @return:
        '''
        current_payload = self.all_task.get()
        # 1自定义封包阶段
        headers = {}
        try:
            # 2进入发送请求流程
            response = requests.request('GET',current_payload, headers=headers,timeout=3, verify=False,allow_redirects=False)
            # 3进入结果处理流程
            self.responseHandler(response)
        except :
            pass

    def boss(self):
        '''
        @description: worker控制器
        @param {type}
        @return:
        '''
        while not self.all_task.empty():
            self.worker()

    def bruter(self,url):
        '''
        @description: 扫描插件入口函数
        @param {url:目标}
        @return:
        '''
        # 自动识别404-预先获取404页面特征
        i = Inspector(url)
        (result, notfound_type) = i.check_this()
        if notfound_type == Inspector.TEST404_MD5 or notfound_type == Inspector.TEST404_OK:
            self.autodiscriminator_md5.add(result)

        # 加载payloads
        payloads = self.scanModeHandler(url)

        # payload入队task队列
        for payload in payloads:
            url_payload = url + payload
            # payload入队，等待处理
            self.all_task.put(url_payload)

        # 循环任务数不能一次性取完所有的task，暂时采用每次执行30个任务。
        while not self.all_task.empty():
            all_task = [gevent.spawn(self.boss) for i in range(30)]
            gevent.joinall(all_task)

    def scan(self):
        self.bruter(self.url)

    def save(self, urls):
        Sqldb(self.dbname).get_urls(urls)

    def pool(self):
        gevent.spawn(self.scan())
        self.save(self.outjson)

if __name__ == '__main__':
    test = DirScan('https://www.baidu.com')
    test.pool()
