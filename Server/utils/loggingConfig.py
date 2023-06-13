import logging
import os
import time
from pathlib import Path


logFileName = "Server"
logsDirPath = os.path.join(Path(__file__).resolve().parent.parent, "logs")
# logFileName = ""
# logsDirPath = ""

filename = os.path.join(logsDirPath, f"{logFileName}_{time.strftime('%Y%m%d')}.log")

logger = logging.getLogger()

# 设置日志等级
logger.setLevel(logging.DEBUG)

# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s %(filename)s %(funcName)s line:%(lineno)d %(levelname)s %(message)s"
)

# 将日志输出至控制台
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

# 将日志输出至文件
fileHandler = logging.FileHandler(filename=filename)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# 阻断向父logger的传播
logger.propagate = False


# if __name__ == '__main__':
    # logger.info("")