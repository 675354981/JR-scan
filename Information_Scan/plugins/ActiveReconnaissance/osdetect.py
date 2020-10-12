import nmap
import xml
from lib.cli_output import console

def osdetect(ip):   #识别操作系统
    nm = nmap.PortScanner()   #实例化
    try:
        result = nm.scan(hosts=ip, arguments='-sS -O -vv -n -T4 -p 80,22,443')   #参数设置
        for k, v in result.get('scan').items():   
            if v.get('osmatch'):
                for i in v.get('osmatch'):
                    console('OSdetect', ip, i.get('name') + '\n')  #显示
                    return i.get('name')   #返回操作系统名称
            else:
                break
    except Exception as e:
        console('OSdetect', ip, 'None\n')

if __name__ == "__main__":
    os = osdetect('127.0.0.1')
