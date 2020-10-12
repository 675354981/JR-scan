import hashlib
import random
import sys
import urllib
import requests

USER_AGENT = "Mozilla/5.0 (Windows; U; MSIE 10.0; Windows NT 9.0; es-ES)"
user_agent = {"user-agent": USER_AGENT}

class Inspector:
    """ 这个类的任务是在运行时检查应用程序的行为

        目的:请求一个不存在的页面"""
    TEST404_OK = 0
    TEST404_MD5 = 1
    TEST404_STRING = 2
    TEST404_URL = 3
    TEST404_NONE = 4

    def __init__(self, target):
        self.target = target

    def _give_it_a_try(self):
        """每次调用此方法时，它都会请求一个随机资源

            目标域。返回值是一个值为的字典

            HTTP响应代码，resquest大小，md5的内容和内容

            本身。如果有重定向，它将记录新的url"""

        s = []
        for n in range(0, 42):
            random.seed()
            s.append(chr(random.randrange(97, 122)))
        s = "".join(s)

        target = self.target + s

        try:
            page = requests.get(target, headers=user_agent, verify=False,timeout=5)
            content = page.content
            result = {
                    'target': urllib.parse.urlparse(target).netloc,
                    'code': str(page.status_code),
                    'size': len(content),
                    'md5': hashlib.md5(content).hexdigest(),
                    'content': content,
                    'location': None
                }
            if len(page.history) >= 1:
                result['location'] = page.url
            return result
        except:
            result = {
                    'target': urllib.parse.urlparse(target).netloc,
                    'code': '',
                    'size': '',
                    'md5': '',
                    'content': '',
                    'location': None
                }
            return result

    def check_this(self):
        """Get the a request and decide what to do"""
        first_result = self._give_it_a_try()

        if first_result['code'] == '404':
            return '', Inspector.TEST404_OK

        elif first_result['code'] == '302' or first_result['location']:
            location = first_result['location']
            return location, Inspector.TEST404_URL
        else:
            return first_result['md5'], Inspector.TEST404_MD5

        return '', Inspector.TEST404_NONE

if __name__ == '__main__':
    i = Inspector(sys.argv[1])
    print(i.check_this())
