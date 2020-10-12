import geoip2.database   
import geoip2.errors
from lib.cli_output import console  #目标展示

def geoip(ipaddr):
    # 获取IP地理位置
	#geoip2查询ip的详细地址信息
    try:
        reader = geoip2.database.Reader('Information_Scan/data/GeoLite2-City.mmdb')   #分析IP颗粒度  读取数据库
        response = reader.city(ipaddr)   #解析正常的IP物理地址赋值给response
        country = response.country.names["zh-CN"]  #解析成为中文   国家
        site = response.subdivisions.most_specific.names["zh-CN"]   #省份
        if not site:
            site = ''
        city = response.city.names["zh-CN"]  #城市
        if not city:
            city = ''
        address = '{} {} {}'.format(country, site, city)  #国家 省份 城市
    except FileNotFoundError:
        address = 'Geoip File Not Found'
    except (KeyError, geoip2.errors.AddressNotFoundError):
        address = 'Address Not In Databases'
    except Exception as e:
        address = 'None'
    console('GeoIP', ipaddr, 'Address: {}\n'.format(address))   #结果显示
    console('GeoIP', ipaddr, 'Ipaddr: {}\n'.format(ipaddr))   
    return address   #返回目标物理地址

if __name__ == "__main__":
    geoip('1.1.1.1')
