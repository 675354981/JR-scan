import re
import json
from bs4 import BeautifulSoup


class WebPage(object):
    """
	网页的简单表示，解耦
	来自任何特定的HTTP库的API。
    """
    def __init__(self, url, html, headers):
        """
		
        初始化一个新的网页对象。
		参数
		----------
		url: str
		web页面URL。
		html: str
		网页内容(HTML)
		标题:dict类型
		HTTP响应头信息
		
        """
        # if use response.text, could have some error
        self.html = html   #session返回的网站主体源码
        self.url = url
        self.headers = headers

        # Parse the HTML with BeautifulSoup to find <script> and <meta> tags.
		
        self.parsed_html = soup = BeautifulSoup(self.html, "html.parser")    #BeautifulSoup解析网站
		
        self.scripts = [script['src'] for script in soup.findAll('script', src=True)]    #列表推导式   获取src
		
        self.meta = {                           #{'dt': 'qw123ewe','coneqwewe123tent': 'qwe123we'}
            meta['name'].lower(): meta['content']
            for meta in soup.findAll('meta', attrs=dict(name=True, content=True))
        }

        self.title = soup.title.string if soup.title else 'None'
        self.title = re.sub(r'^\s+', '', self.title)  #标题开头是空子节的
		
        wappalyzer = Wappalyzer()   #实例化
        self.apps = wappalyzer.analyze(self)   #返回应用程序列表
        self.result = ';'.join(self.apps)   #添加入;

    def check(self):   #检查cms类型
        out = []
        apps = []
        try:
            with open('Information_Scan/data/apps.txt', 'r', encoding='utf-8') as f:
                for i in f.readlines():
                    apps.append(i.strip('\n'))

            for i in apps:
                name, method, position, regex = i.strip().split("|", 3)    #分割三次
                if method == 'headers':
                    if self.headers.get(position) != None:
                        if re.search(regex, str(self.headers.get(position))) != None:
                            out.append(name)
                elif method == 'index':
                    if re.search(regex, self.html):
                        out.append(name)
                elif method == 'match':
                    for k, v in self.headers.items():
                        if regex in v or regex in k:
                            out.append(name)
                else:
                    if regex in self.html:
                        out.append(name)
        except Exception as e:
            pass
        return out   #返回cms类型

    def info(self):   #返回cms信息
        result = self.result.split(';')   #以;进行切割
        result.extend(self.check())    #增加cms信息列表
        try:
            server = self.headers['Server']
        except:
            server = 'None'

        result = list(filter(None, result))   #filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表

        programs = ['PHP', 'JSP', 'ASP', 'Node.js', 'ASPX', 'Ruby', 'Python', 'Go']   #编程语言
        middles = [
            'Nginx', 'Apache', 'Apache Tomcat', 'IIS', 'Jetty', 'JBoss', 'Weblogic', 'WebSphere', 'IIS8.0', 'IIS6.0',
            'IIS7.0', 'lighttpd', 'mod_fastcgi', 'Caddy'
        ]

        return {
            "apps": list(set(result)),   #cms信息
            "title": self.title,   #网站标题
            "server": server,   #服务器名称
        }


class Wappalyzer(object):
    """
    Python Wappalyzer driver.
    """
    def __init__(self, apps_file=None):
        """
        初始化一个新的Wappalyzer实例。
		参数
		----------
		类别:dict类型
		将类别id映射到名称，如在apps.json中。
		应用:dict类型
		app名称到app dicts的映射，如apps.json。
        """
        if apps_file:
            with open(apps_file, 'rb') as fd:
                obj = json.load(fd)    #导入
        else:
            with open("Information_Scan/data/apps.json", 'rb') as fd:
                obj = json.load(fd)   #导入  json格式

        self.categories = obj['categories']    #相关cms名称
        self.apps = obj['apps']       #相关cms标志

        for name, app in self.apps.items():         #items() 函数以列表返回可遍历的(键, 值) 元组数组。
            self._prepare_app(app)    #cms头信息

    def _prepare_app(self, app):  #正则编译结果
	
        """
        对app数据进行归一化，为检测阶段做准备。
        """

        # Ensure these keys' values are lists
        for key in ['url', 'html', 'script', 'implies']:   #依次赋值
            value = app.get(key)
            if value is None:
                app[key] = []
            else:
                if not isinstance(value, list):   #来判断一个对象是否是一个已知的类型，类似 type()   但是会考虑继承关系
                    app[key] = [value]  #将value强行转为列表   json格式

        # 确定键值存在
        for key in ['headers', 'meta']:
            value = app.get(key)
            if value is None:
                app[key] = {}

        # 确保“meta”键是dict
        obj = app['meta']
        if not isinstance(obj, dict):   #如果不是字典
            app['meta'] = {'generator': obj}

        # 确保键是小写的
        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}

        # 准备正则表达式模式
        for key in ['url', 'html', 'script']:
            app[key] = [self._prepare_pattern(pattern) for pattern in app[key]]   #url html script以此带入进行正则表达式编译并写入列表

        for key in ['headers', 'meta']:
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = self._prepare_pattern(obj[name])   #返回正则编译结果

    def _prepare_pattern(self, pattern):   #负责正则预编译
        """
        从模式中提取值对并编译正则表达式。
        """
        regex, _, rest = pattern.partition('\\;')   #partition() 方法用来根据指定的分隔符将字符串进行分割。
        try:
            return re.compile(regex, re.I)   #返回正则编译   
        except re.error as e:    #有问题
            return re.compile(r'(?!x)x')

    def _has_app(self, app, webpage):   #返回签名状态
        """
        确定web页面是否与应用程序签名匹配。
        """
        for regex in app['url']:
            if regex.search(webpage.url):  #进行匹配
                return True

        for name, regex in app['headers'].items():
            if name in webpage.headers:
                content = webpage.headers[name]
                if regex.search(content):
                    return True

        for regex in app['script']:
            for script in webpage.scripts:
                if regex.search(script):
                    return True

        for name, regex in app['meta'].items():
            if name in webpage.meta:
                content = webpage.meta[name]
                if regex.search(content):
                    return True

        for regex in app['html']:
            if regex.search(webpage.html):
                return True

    def _get_implied_apps(self, detected_apps):
	
        """
        获取' detected_apps '中隐藏数据。
        """
		
        def __get_implied_apps(apps):   #获取相应cms数据
            _implied_apps = set() 
            for app in apps:
                if 'implies' in self.apps[app]:     #判断implies (cms语言)是不是存在，如在的话加入到集合
                    _implied_apps.update(set(self.apps[app]['implies']))
            return _implied_apps

        implied_apps = __get_implied_apps(detected_apps)
        all_implied_apps = set()   #更新集合

        # 递归下降，直到找到所有隐含的应用程序
        while not all_implied_apps.issuperset(implied_apps):   #issuperset() 判断指定集合的所有元素是否都包含在原始的集合中。
            all_implied_apps.update(implied_apps)   #添加implied_apps中的元素到all_implied_apps中去
            implied_apps = __get_implied_apps(all_implied_apps)

        return all_implied_apps   #返回cms数据

    def get_categories(self, app_name):  #对象cms信息
        """
        Returns a list of the categories for an app name.
        """
        cat_nums = self.apps.get(app_name, {}).get("cats", [])
        cat_names = [self.categories.get("%s" % cat_num, "") for cat_num in cat_nums]

        return cat_names

    def analyze(self, webpage):
        """
        返回可在web页面上检测到的应用程序列表。
        """
        detected_apps = set()   #设成集合，防止重复

        for app_name, app in self.apps.items():    #得到数据
            if self._has_app(app, webpage):  #cms信息匹配检测
                detected_apps.add(app_name)   #匹配成功  cms名字  1C-Bitrix

        detected_apps |= self._get_implied_apps(detected_apps)    #按位或运算 去重  1|1 =1   1|0 =0   0|0 = 0

        return detected_apps   #返回cms列表

    def analyze_with_categories(self, webpage):
        detected_apps = self.analyze(webpage)  #确定cms
        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            categorised_apps[app_name] = {"categories": cat_names}

        return categorised_apps  #cms信息
