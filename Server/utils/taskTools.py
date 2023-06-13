import threading
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


class Task:
    """
    任务类
    """

    def __init__(self, fun, taskName):
        """
        任务实例初始化
        :param fun: 任务函数逻辑
        :param taskName: 任务名
        """

        # 任务函数
        self.fun = fun

        # 任务名
        self.taskName = taskName

        # 任务携带的信息
        self.carry = None

        # 所属任务池
        self.taskPool = None

        # 任务是否正在运行
        self.running = False

        # 任务是否已完成
        self.completed = False

        # 任务是否发生异常
        self.error = None

        # 任务完成后的返回值
        self.result = None

        # 任务线程执行的Future对象
        self.future = None

    def __call__(self, *args, **kwargs):
        """
        实现把Task实例对象直接当作函数调用
        执行任务代码
        :param args:
        :param kwargs:
        :return: 函数返回值
        """

        # 任务开始执行
        self.running = True

        try:
            self.result = self.fun(*args, **kwargs)
        except BaseException as e:
            self.error = e

        # 任务结束
        self.__done()

        return self.result

    def __done(self):
        """
        任务结束
        """

        # 任务结束运行
        self.running = False
        # 任务完成
        self.completed = True

        # 任务出池
        if self.taskPool:
            self.taskPool.outTaskPool(self)

        print(f"【任务（{self.taskName}）】：{f'发生异常：{self.error}' if self.error else '已完成'}")


class TaskPool:
    """
    任务池
    入池对象：Task实例对象

    功能：
    1.调节任务并发数量，池满则阻塞入池
    2.监控Task任务完成情况，完成则出池
    """

    def __init__(self, maxPoolSize, taskPoolName):
        """
        任务池初始化
        :param maxPoolSize: 任务池大小
        :param taskPoolName: 任务池名
        """

        # 任务池名
        self.taskPoolName = taskPoolName

        # 创建池的最大任务数量
        self.maxPoolSize = maxPoolSize

        # 是否阻塞入池
        self.blockPutTaskStatus = False

        """
        任务池
        利用列表的循环遍历，可任意获取某任务
        可看作该列表为池
        """
        self.taskPool = []
        # 创建任务池的互斥锁
        self.__taskPoolLock = threading.Lock()

        """
        用于任务池的计数
        利用队列的特性，实现对任务池：
        1.若池满，则阻塞put
        2.若池空，则阻塞get
        """
        self.__countQueue = Queue(maxsize=self.maxPoolSize)

    def putTask(self, task):
        """
        提交任务入池
        1.如果任务池未满，则countQueue.put不会阻塞，其任务数 +1，进而taskPool.append +1
        2.如果任务池满，则countQueue.put阻塞，直到未满进而继续入池
        :param task: Task实例对象
        :return:
        """

        # 检查传入task类型是否正确
        if not isinstance(task, Task):
            raise TypeError("参数类型异常: task需为Task实例对象")

        # 检查是否阻塞入池
        while self.blockPutTaskStatus:
            time.sleep(0.5)

        # 任务数+1
        self.__countQueue.put(task)

        # 任务入池
        with self.__taskPoolLock:
            self.taskPool.append(task)

        # 关联所属任务池
        task.taskPool = self

        print(f"【任务池（{self.taskPoolName}）】：{task.taskName} 入池")

    def allowPutTask(self):
        """
        允许继续入池
        @return: 阻塞状态
        """
        self.blockPutTaskStatus = False
        return self.blockPutTaskStatus

    def blockPutTask(self):
        """
        阻塞继续入池
        @return: 阻塞状态
        """
        self.blockPutTaskStatus = True
        return self.blockPutTaskStatus

    def outTaskPool(self, task):
        """
        将任务对象出池
        """

        # 检查传入task类型是否正确
        if not isinstance(task, Task):
            raise TypeError("参数类型异常: task需为Task实例对象")

        if not task.taskPool:
            raise Exception("task不处于任务池中，无法出池")

        if task.running:
            raise Exception("task正在运行中，无法出池")

        # 1. 任务池出池
        with self.__taskPoolLock:
            self.taskPool.remove(task)
        # 2. 任务计数队列 -1
        self.__countQueue.get()

        """
        任务计数队列 任务完成数+1
        当 完成数 加至等于 入队数时，countQueue.join()终止阻塞
        """
        print(f"【任务池（{self.taskPoolName}）】：{task.taskName} 出池")
        print(
            f"【任务池（{self.taskPoolName}）】：剩余 {self.__countQueue.qsize()} 个任务 {[task.taskName for task in self.taskPool]}")
        self.__countQueue.task_done()

    def wait(self):
        """
        等待所有任务完成
        """
        return self.__countQueue.join()

    def taskPoolSize(self):
        """
        任务池大小
        """
        return self.__countQueue.qsize()


class TaskPoolExecutor(TaskPool):
    """
    任务池执行器
    入池对象：Task实例对象

    功能：
    1.调节任务并发数量，池满则阻塞入池
    2.监控Task任务完成情况，完成则出池
    3.入池Task对象自动执行（入池则开始执行）
    """

    def __init__(self, maxThreadSize, taskPoolName):
        """
        初始化
        """

        super(TaskPoolExecutor, self).__init__(maxPoolSize=maxThreadSize, taskPoolName=taskPoolName)

        # 初始化线程池
        self.maxThreadSize = maxThreadSize
        self.__threadPool = ThreadPoolExecutor(max_workers=self.maxThreadSize)

    def runTask(self, task, *args, **kwargs):

        # 检查传入task类型是否正确
        if not isinstance(task, Task):
            raise TypeError("参数类型异常: task需为Task实例对象")

        if task not in self.taskPool:
            raise Exception("task任务未入池，无法启动")

        # 提交至线程池异步执行
        if not self.__threadPool._shutdown:
            task.future = self.__threadPool.submit(task, *args, **kwargs)
        else:
            self.outTaskPool(task=task)

        return task

    def putAndRunTask(self, task, *args, **kwargs):
        """
        增加任务并启动
        池满将阻塞
        :param task: task实例对象
        :param args: 请求参数表列
        :param kwargs: 请求参数表列
        :return: task实例对象
        """

        # 任务入池
        self.putTask(task)

        # 运行任务
        task = self.runTask(task=task, *args, **kwargs)

        return task
