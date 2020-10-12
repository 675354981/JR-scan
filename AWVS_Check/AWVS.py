import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lib.setting import apikey
from lib.cli_output import console
from lib.bcolors import Bcolors

class awvs():
    def __init__(self):
        self.task = []
        self.server = 'https://127.0.0.1:13443/'
        self.header = {'X-Auth': apikey, 'content-type': 'application/json'}
        # 前6个为系统默认扫描策略，后面为自定义
        self.scan_rule = {
            "FS": "11111111-1111-1111-1111-111111111111",
            "HR": "11111111-1111-1111-1111-111111111112",
            "XSS": "11111111-1111-1111-1111-111111111116",
            "SQL": "11111111-1111-1111-1111-111111111113",
            "WP": "11111111-1111-1111-1111-111111111115",
            "CO": "11111111-1111-1111-1111-111111111117"
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def request(self, path):
        try:
            return requests.get(url=self.server + path, timeout=10, verify=False, headers=self.header)
        except Exception as e:
            print(e)

    def scan_type(self):
        # 扫描策略选择
        try:
            l = '[0] Full Scan\n'
            l += '[1] High Risk Vulnerabilities\n'
            l += '[2] Cross-site Scripting Vulnerabilities\n'
            l += '[3] SQL Injection Vulnerabilities\n'
            l += '[4] Weak Passwords\n'
            l += '[5] Crawl Only'
            print(Bcolors.BLUE + l + Bcolors.ENDC)
            rule = input(Bcolors.RED + '[JR/AWVS_Check/Set_Rule]>> ' + Bcolors.ENDC)
            if rule == '0':
                return self.scan_rule['FS']
            elif rule == '1':
                return self.scan_rule['HR']
            elif rule == '2':
                return self.scan_rule['XSS']
            elif rule == '3':
                return self.scan_rule['SQL']
            elif rule == '4':
                return self.scan_rule['WP']
            elif rule == '5':
                return self.scan_rule['CO']
            else:
                #console('JR/AWVS_Check','策略扫描','输入有误')
                print(Bcolors.WARNING + '[-] Ops, 输入有误...' + Bcolors.ENDC)
        except Exception as e:
            print(e)

    def check_id(self):
        # 扫描任务ID选择
        try:
            r = self.request('api/v1/scans')
            response = json.loads(r.text)
            text = response['scans']
            if len(text) > 0:
                for i in range(len(text)):
                    self.task.append(text[i]['scan_id'])
                    print(Bcolors.GREEN + '[' + str(i) + ']', text[i]['target']['address'] + Bcolors.ENDC)
                task_id = input(Bcolors.RED + '[JR/AWVS_Check/Set_Task_Id]>> ' + Bcolors.ENDC)
                return self.task[int(task_id)]
            else:
                #console('JR/AWVS_Check', '任务清单', '当前无扫描任务')
                print(Bcolors.GREEN + '[-] Ops, 当前无扫描任务...' + Bcolors.ENDC)
                return
        except Exception as e:
            #console('JR/AWVS_Check', '任务清单', '输入有误')
            print(Bcolors.WARNING + '[-] Ops, 输入有误...' + Bcolors.ENDC)
        finally:
            # 清空获取的任务列表
            del self.task[:]

    def add(self):
        # 添加扫描对象
        try:
            target = input(Bcolors.RED + '[JR/AWVS_Check/Set_Target]>> ' + Bcolors.ENDC)
            data = {'address': target, 'description': target, 'criticality': '10'}
            r = requests.post(url=self.server + 'api/v1/targets', timeout=10,
                              verify=False, headers=self.header, data=json.dumps(data))
            # print(r.status_code)
            if r.status_code == 201:
                # print('添加成功')
                return json.loads(r.text)['target_id']
        except Exception as e:
            print(e)

    def scan(self):
        # 启动扫描任务
        data = {'target_id': self.add(), 'profile_id': self.scan_type(),
                'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
        try:
            r = requests.post(url=self.server + 'api/v1/scans', timeout=10, verify=False, headers=self.header,
                              data=json.dumps(data))
            if r.status_code == 201:
                print(Bcolors.GREEN + '[-] OK, 扫描任务已经启动...' + Bcolors.ENDC)
        except Exception as e:
            print(e)

    def stop(self):
        # 停止扫描任务
        try:
            r = requests.post(url=self.server + 'api/v1/scans/' + self.check_id() + '/abort',
                              timeout=10, verify=False, headers=self.header)
            if r.status_code == 204:
                print(Bcolors.GREEN + '[-] OK, 扫描已经停止...' + Bcolors.ENDC)
        except Exception as e:
            pass

    def view(self):
        # 查看任务状态
        try:
            r = self.request('api/v1/scans/' + self.check_id())
            response = json.loads(r.text)
            addr = response['target']['address']
            high = response['current_session']['severity_counts']['high']
            medium = response['current_session']['severity_counts']['medium']
            low = response['current_session']['severity_counts']['low']
            status = response['current_session']['status']
            print(u'[-] 扫描目标: {}'.format(addr))
            print(u'[-] 扫描状态: {}'.format(status))
            print(u'[-] 高危漏洞: {}'.format(high))
            print(u'[-] 中危漏洞: {}'.format(medium))
            print(u'[-] 低危漏洞: {}'.format(low))
        except Exception as e:
            pass

    def delete(self):
        # 删除扫描任务
        try:
            r = requests.delete(url=self.server + 'api/v1/scans/' + self.check_id(),timeout=10, verify=False, headers=self.header)
            if r.status_code == 204:
                print(Bcolors.GREEN + '[-] OK, 已经删除任务...' + Bcolors.ENDC)
        except Exception as e:
            pass

    def usage(self):
        s = '帮助:\n'
        s += '    scan        任务创建\n'
        s += '    stop        任务停止\n'
        s += '    delete      任务删除\n'
        s += '    view        任务进度\n'
        s += '    back        返回列表\n'
        print(Bcolors.BLUE + s + Bcolors.ENDC)

if __name__ == '__main__':
    mywvs = awvs()
    mywvs.usage()


