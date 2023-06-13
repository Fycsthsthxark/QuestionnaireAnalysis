import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from utils.loggingConfig import logger
from utils.taskTools import TaskPoolExecutor, Task


class Executor(TaskPoolExecutor):
    """
    执行器父类
    """

    def __init__(self, maxThreadSize):
        # Scheduler定时任务
        self.schedulerJob = None

        # 最后一次启动时间
        self.lastStartTime = None

        # 执行器名 (执行器的唯一ID)
        self.executorName = self.__class__.__name__

        # 执行器父类名
        self.executorBaseName = self.__class__.__base__.__name__

        super(Executor, self).__init__(maxThreadSize=maxThreadSize, taskPoolName=self.executorName)

    def executorEvent(self):
        """
        执行器运行逻辑
        用于子类重写业务逻辑
        @return:
        """
        pass

    def formatExecutorEventToTask(self):
        """
        格式化执行器业务逻辑
        @return: Task任务对象
        """

        def taskFun():
            self.executorEvent()
            self.wait()

        task = Task(fun=taskFun, taskName=self.executorName)
        task.carry = self
        return task


class ExecutorManager(TaskPoolExecutor):
    """
    执行器管理器
    """

    def __init__(self, maxThreadSize, taskPoolName):

        super(ExecutorManager, self).__init__(maxThreadSize=maxThreadSize, taskPoolName=taskPoolName)

        # 注册的Executor
        self.executorPool = list()

        # 定义定时任务
        logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
        self.executorBackgroundScheduler = BackgroundScheduler(timezone="Asia/Shanghai", daemon=True)
        self.executorBackgroundScheduler.start()

    def registerExecutor(self, ExecutorClass):
        """
        注册已有的Executor子类
        @param ExecutorClass: Executor的子类（class）
        """
        if not issubclass(ExecutorClass.__base__, Executor):
            logger.error("ExecutorClass应为Executor子类")
            raise TypeError

        executor = ExecutorClass()
        if self.findExecutor(executor.executorName):
            logger.error(f"{executor.executorName}实例已注册，不能重复注册")
            raise Exception
        self.executorPool.append(executor)

    def findExecutor(self, executorName):
        """
        通过executorName在executorPool寻找对象
        @param executorName: executor名
        @return: 该对象 or None
        """
        for executor in self.executorPool:
            if executor.executorName == executorName:
                return executor
        return None

    def executorIsRunning(self, executor):
        """
        判断executor任务是否已处于任务池（不论其暂停与否）
        @param executor: Executor的实例对象
        @return: True or False
        """

        if not isinstance(executor, Executor):
            logger.error("executor应为Executor实例对象")
            raise TypeError

        for task in self.taskPool:
            if task.carry == executor:
                return True
        return False

    def runExecutor(self, executor):
        """
        开始运行executor
        @param executor: Executor实例对象
        """
        if not isinstance(executor, Executor):
            logger.error("executor应为Executor实例对象")
            raise TypeError

        if self.executorIsRunning(executor=executor):
            logger.warning(f"{executor.executorName}已启动于任务池，等待其结束才能再次启动")
            return

        self.putAndRunTask(task=executor.formatExecutorEventToTask())
        executor.lastStartTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getExecutorSchedulerJobTime(self, executor):
        """
        得到executor定时任务的时间
        @param executor: Executor实例对象
        @return: {"hour": hour, "minute": minute} or None
        """
        if not isinstance(executor, Executor):
            raise TypeError("executor应为Executor实例对象")

        if not executor.schedulerJob:
            return None

        seconds = executor.schedulerJob.trigger.__getstate__()["interval"].seconds
        minute = seconds / 60
        hour = (minute - minute % 60) / 60
        minute = minute % 60
        return {"hour": hour, "minute": minute}

    def addExecutorScheduler(self, executor, hour, minute):
        """
        增加executor的定时任务
        @param hour: 小时
        @param minute: 分钟
        @param executor: Executor实例对象
        """
        if not isinstance(executor, Executor):
            logger.error("executor应为Executor实例对象")
            raise TypeError

        # 先取消已存在的定时任务
        self.removeExecutorScheduler(executor=executor)

        # 新建定时任务
        seconds = (int(hour) * 60 + int(minute)) * 60
        schedulerJob = self.executorBackgroundScheduler.add_job(self.runExecutor, "interval",
                                                                kwargs={"executor": executor}, seconds=seconds)
        executor.schedulerJob = schedulerJob
        logger.info(f"{executor.executorName}新增定时任务,每间隔{hour}小时{minute}分钟后执行一次")

    def removeExecutorScheduler(self, executor):
        """
        移除executor的定时任务
        @param executor: Executor实例对象
        @return:
        """
        if not isinstance(executor, Executor):
            logger.error("executor应为Executor实例对象")
            raise TypeError

        if executor.schedulerJob:
            executor.schedulerJob.remove()
            logger.info(f"{executor.executorName}已删除{executor.schedulerJob}的定时任务")
            executor.schedulerJob = None
