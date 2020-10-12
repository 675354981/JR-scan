import random
import socket
import string
import struct
from fake_useragent import UserAgent

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': "",
    'Referer': "",
    'X-Forwarded-For': "",
    'X-Real-IP': "",
    'Connection': 'keep-alive',
}

def get_ua():   #自定义headers头
    ua = []
    with open(r'Information_Scan/data/path/user-agents.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            ua.append(i.strip())  # 形成路径 每行进行切换

    key = random.random() * 20  #随机值
    referer = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(int(key))])  #生成随机referer
    referer = 'www.' + referer.lower() + '.com'
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))  #转换IPV4地址字符串（192.168.10.8）成为32位打包的二进制格式  
    #struct.pack  按照给定的格式(fmt)，把数据封装成字符串
    HEADERS["User-Agent"] = random.choice(ua)
    HEADERS["Referer"] = referer
    HEADERS["X-Forwarded-For"] = HEADERS["X-Real-IP"] = ip

    return HEADERS


if __name__ == "__main__":
    print(get_ua())

