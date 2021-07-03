import time


def time_to_int(time_string):
    """
    时间格式转换成时间戳
    :param time_string:
    """
    return int(time.mktime(time.strptime(time_string, "%Y-%m-%d %H:%M:%S")))
