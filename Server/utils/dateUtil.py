import datetime


def getNowTimeStamp():
    """
    得到当前时间的时间戳
    """
    return str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))


def getSpecifyTimeStamp(year: int, month: int = None, day: int = None, hour: int = 0, minute: int = 0, second: int = 0):
    """
    得到指定时间的时间戳
    """
    return int((datetime.datetime(year=year,
                                  month=month,
                                  day=day,
                                  hour=hour,
                                  minute=minute,
                                  second=second
                                  ) - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def timeStampToDateDict(timeStamp):
    """
    时间戳转日期字典
    """
    date = datetime.datetime.fromtimestamp(timeStamp / 1000)
    return {"year": date.year, "month": date.month, "day": date.day, "hour": date.hour,
            "minute": date.minute, "second": date.second}
