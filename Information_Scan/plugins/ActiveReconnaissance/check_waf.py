import re
from Information_Scan.Requests import Requests
from Information_Scan.waf import WAF_RULE

'''
WAF 检测思路

发送Payload触发WAF拦截机制，根据响应头字段或者响应体拦截内容判断WAF
'''

payload = (
    "/index.php?id=1 AND 1=1 UNION ALL SELECT 1,NULL,'<script>alert(XSS)</script>',table_name FROM information_schema.tables WHERE 2>1--/**/",
    "/../../../etc/passwd", "/.git/", "/phpinfo.php")


def verify(headers, content):       #检测有无WAF
    for i in WAF_RULE:
        name, method, position, regex = i.split('|')   #提取触发waf的名字 方式 服务 被什么拦截
        if method == 'headers':
            if headers.get(position) is not None:    #CacheFly CDN|headers|BestCDN|CacheFly'
                if re.search(regex, str(headers.get(position))) is not None:
                    return name
        else:
            if re.search(regex, str(content)):    #从源码中匹配
                return name

    return 'NoWAF'

def checkwaf(url):    #检测是否存在waf的字符串

    result = 'NoWAF'
    
    try:
        req = Requests()   #实例对象
        r = req.get(url)    #发起请求
        result = verify(r.headers, r.text)    #正常请求检测有无WAF
		
        if result == 'NoWAF':      #没有waf存在进行payload校验，检测waf
            for i in payload:
                r = req.get(url + i)
                result = verify(r.headers, r.text)
                if result != 'NoWAF':
                    return result
        else:
            return result
    except (UnboundLocalError, AttributeError):
        pass
    except Exception as e:
        pass

if __name__ == "__main__":
    out = checkwaf('http://127.0.0.1','test')
    print(out)


