import requests
from .taskTools import Task, TaskPoolExecutor


class Request:
    """
    请求类
    """

    def __init__(self):
        """
        请求实例初始化
        """

        """
        请求方式
        默认不使用session()
        """
        self.__request = requests

    def get(self, *args, **kwargs):
        """
        GET请求
        :param args:
        :param kwargs:
        :return: response
        """
        return self.__request.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        POST请求
        :param args:
        :param kwargs:
        :return: response
        """
        return self.__request.post(*args, **kwargs)

    def session(self):
        """
        使用session()
        :return: 当前实例对象
        """

        # 修改请求方式为使用session()
        self.__request = requests.session()
        return self


class RequestThread(TaskPoolExecutor):
    """
    使用线程异步的请求类
    在线程池满后，会发生阻塞
    """

    def __init__(self, maxThreadSize, taskPoolName):
        """
        初始化
        """

        super(RequestThread, self).__init__(maxThreadSize=maxThreadSize, taskPoolName=taskPoolName)

        # 初始化请求对象
        self.__request = Request()

    def request(self):
        """
        返回单线程请求方式
        """
        return self.__request

    def get(self, callback, *args, **kwargs):
        """
        发起异步GET请求
        :param callback: 请求回调函数
        :param args: 请求参数表列
        :param kwargs: 请求参数表列
        :return: task实例对象
        """
        return self.__runTask(requestMethod="GET", callback=callback, *args, **kwargs)

    def post(self, callback, *args, **kwargs):
        """
        发起异步POST请求
        :param callback: 请求回调函数
        :param args: 请求参数表列
        :param kwargs: 请求参数表列
        :return: task实例对象
        """
        return self.__runTask(requestMethod="POST", callback=callback, *args, **kwargs)

    def session(self):
        """
        使用session()
        :return: 当前实例对象
        """

        # 修改请求方式为使用session()
        self.__request = self.__request.session()
        return self

    def __runTask(self, requestMethod, callback, *args, **kwargs):
        """
        构建请求任务并启动
        :param requestMethod: 请求方式
        :param callback: 请求回调函数
        :param args: 请求参数表列
        :param kwargs: 请求参数表列
        :return: task实例对象
        """

        # 得到对应的请求方式
        if requestMethod == "GET":
            request = self.__request.get
        else:
            request = self.__request.post

        """
        构建任务函数
        无论请求失败与否，都会执行回调函数，传入一个标准的requests.Response()对象
        如有错误则在Task实例结束时报出异常
        """
        def fun(*args, **kwargs):
            response = request(*args, **kwargs)
            callback(response)

        # 创建任务对象
        proxies_format_url = kwargs.get("proxies")
        task_name = kwargs.get("url")
        if not task_name:
            task_name = args[0]
        if proxies_format_url:
            task_name += " -> " + proxies_format_url["http"]
        task = Task(fun=fun, taskName=task_name)

        # 任务入池并运行
        self.putAndRunTask(task=task, *args, **kwargs)

        return task
