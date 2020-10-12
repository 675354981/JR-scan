# 全局超时时间
TIMEOUT = 5

# 设置扫描线程
THREADS = 100

# 如果存在于结果db中就跳过
CHECK_DB = False

# ping探测
PING = True

# 设置cookie
COOKIE = 'random'
# COOKIE = {'Cookie': 'SRCtest'}

#awvs api
apikey='1986ad8c0a5b3df4d7028d5f3c06e936ccf47470c374d42f3a38c950f4bc80394'

# subdomain dir
sub_dict = 'Information_Scan/data/path/wydomain.csv'
next_sub_dict = 'Information_Scan/data/path/next_sub_full.txt'
cnd_dict = 'Information_Scan/data/path/cdn_servers.txt'

#async dir
dir = 'Information_Scan/data/path/dir.txt'

# 目录扫描模式
dict_mode = 1

# 递归爬取模式
crawl_mode = 1

# 设置代理
# SOCKS5 = ('127.0.0.1', 1080)
SOCKS5 = ()

#递归扫描的目录
crawl_mode_parse_html =  "//*/@href | //*/@src | //form/@action"
