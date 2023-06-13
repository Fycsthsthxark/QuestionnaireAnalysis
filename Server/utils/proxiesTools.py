import random
import re
import threading
import time
from bs4 import BeautifulSoup
from utils.requestTools import RequestThread, Request


class Proxies:
    """
    代理类
    每个代理为该类的实例化对象
    """

    def __init__(self, url):
        """
        初始化
        :param url: 代理URL: 例：135.124.32:8080
        """
        # 代理的URL
        self.url = url
        # 格式化URL
        self.proxies = {
            "http": "http://" + self.url,
            "https": "http://" + self.url,
        }

        # 代理是否可用
        self.available = False


class ProxiesManager(RequestThread):
    """
    代理管理器
    传入的代理自动进行持续性验证
    在代理池满后，会发生putProxies传入阻塞
    每个任务为Task对象
    池中每个Task任务的carry属性为Proxies对象
    """

    def __init__(self, maxPoolSize, verifyUrl):
        """
        初始化代理管理器
        :param maxPoolSize: 最大代理池数量
        :param verifyUrl: 验证代理的URL
        """

        super(ProxiesManager, self).__init__(maxThreadSize=maxPoolSize, taskPoolName="代理池")

        # 定时检验代理的时间间隔（s）
        self.timing = 10

        # 等待代理响应时间（s）
        self.timeout = 5

        # 验证代理的URL
        self.verifyUrl = verifyUrl

    def start(self, proxiesUrlList, ensureMinUseNum):
        """
        运行代理管理器
        当可用数达标前阻塞,直到达标后异步持续运行
        :param ensureMinUseNum: 确保最少可用数，达标后停止阻塞主线程
        :param proxiesUrlList: 代理URL列表
        """

        if not isinstance(proxiesUrlList, list):
            raise TypeError("参数类型异常: proxiesUrlList为list类型")

        if ensureMinUseNum > self.maxPoolSize:
            raise ValueError("初始可用数 应小于等于 代理池数")

        # 开始提交代理
        while proxiesUrlList and len(self.getAllProxies()) < ensureMinUseNum:
            self.putProxies(url=proxiesUrlList.pop(0))

        """
        异步持续提交代理
        当可用数达标后异步持续提交代理
        使用守护线程，跟随主线程结束而结束
        """
        def fun(proxiesUrlList):
            for proxiesUrl in proxiesUrlList:
                self.putProxies(url=proxiesUrl)

        threading.Thread(target=fun, args=[proxiesUrlList], daemon=True).start()

    def putProxies(self, url):
        """
        向代理池中提交一个代理
        若代理池满，则阻塞
        :param url: 代理URL
        :return: Proxies实例对象
        """

        # 构建代理实例对象
        proxies = Proxies(url=url)

        # 异步持续检验代理可用性的回调函数
        def callback(response):
            """
            第一次异步提交代理检验后的回调函数
            用于在异步线程中持续进行检验
            :param response: 代理请求响应结果
            """

            # 持续进行检验
            while response.status == 200:

                proxies.available = True
                # 定时阻塞
                time.sleep(self.timing)

                try:
                    response = self.__request.get(url=self.verifyUrl, proxies=proxies.proxies, timeout=self.timeout)
                except BaseException as e:
                    proxies.available = False
                    raise e

            proxies.available = False
            raise Exception(f"{proxies.url}代理不可用")

        # 开始异步线程任务池中持续检验
        task = self.get(callback=callback, url=self.verifyUrl, proxies=proxies.proxies,
                                        timeout=self.timeout)
        task.carry = proxies

        return proxies

    def getProxies(self):
        """
        随机得到一个可用的代理
        :return: Proxies对象 or None
        """
        proxies_pool = self.getAllProxies()
        if len(proxies_pool):
            return proxies_pool[random.randint(0, len(proxies_pool) - 1)]
        return None

    def getAllProxies(self):
        """
        得到所有代理池中的可用代理对象
        """

        proxies_pool = []
        for task in self.taskPool:
            proxies = task.carry
            if proxies.available:
                proxies_pool.append(proxies)

        return proxies_pool


class ProxiesParser:
    """
    代理解析器
    用于提取文本或网站中的代理
    """

    def __init__(self):
        # 初始化请求方法
        self.__request = Request()

    def parsesText(self, text):
        """
        解析含有代理的文本
        格式如含有:
        1. 123.13.123.23:8080
        2. 123.13.123.23    8080
        :param text: 含有代理的文本
        :return: 代理URL列表
        """

        # 正则匹配如格式 123.13.123.23:8080
        pattern = re.compile(r'(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]):(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9])')
        proxies_url_list = re.findall(pattern, text)

        # 正则匹配如格式 123.13.123.23   8080
        if not proxies_url_list:
            pattern = re.compile(r'(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\s+(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9])')
            proxies_url_list = re.findall(pattern, text)

        # 格式化成代理URL
        proxies_url_list = [f'{".".join(i[:4])}:{i[-1]}' for i in proxies_url_list]

        return proxies_url_list

    def parsesCrawler(self, url):
        """
        解析代理网站的爬虫逻辑
        :param url: 代理所在网站URL
        :return: 代理URL列表
        """

        proxies_url_list = []
        response = self.__request.get(url=url)
        bs = BeautifulSoup(response.text, "html.parser")
        trs = bs.find("tbody").find_all('tr')[1:]
        for tr in trs:
            proxies_url_list.append(":".join([i.text.strip() for i in tr.find_all("td")[:2]]))

        return proxies_url_list
