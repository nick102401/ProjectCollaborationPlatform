# -*-coding:utf-8-*-
import json
import random
import string
import time
from datetime import datetime, timedelta

from FastApi.common.logs_handle import Logger

log = Logger().logger

"""
辅助方法
"""


def get_value_from_resp(in_dict, target_key, locate_key="", locate_value=".*"):
    """
    根据已知K,V获取另一个K对应的V
    :param in_dict:
    :param target_key:
    :param locate_key:
    :param locate_value:
    :return:
    """
    ret = recursion_search(in_dict, target_key, locate_key, locate_value)
    if ret:
        return ret
    else:
        log.error('get_value_from_resp failed!')
        return False


def recursion_search(in_dict, target_key, locate_key="", locate_value=""):
    """
    递归：根据已知K,V获取另一个K对应的V
    :param in_dict:
    :param target_key:
    :param locate_key:
    :param locate_value:
    :return:
    """
    if isinstance(in_dict, dict):
        for k, v in in_dict.items():
            if isinstance(v, dict):
                ret = recursion_search(v, target_key, locate_key, locate_value)
                if ret:
                    return ret
            elif isinstance(v, list):
                for item in v:
                    ret = recursion_search(item, target_key, locate_key, locate_value)
                    if ret:
                        return ret
            else:
                if locate_key:
                    if k == locate_key and v == locate_value:
                        return in_dict[target_key]
                elif k == target_key:
                    return v
    elif isinstance(in_dict, str):
        in_dict = json.loads(in_dict)
        ret = recursion_search(in_dict, target_key, locate_key, locate_value)
        if ret:
            return ret


def bjs_to_utc(bjs_time):
    """
    北京时间转格林时间
    :param bjs_time:
    :return:
    """
    utc_format = "%Y-%m-%dT%H:%M:%S"
    bjs_format = "%Y-%m-%d %H:%M:%S"
    bjs_time = datetime.strptime(bjs_time, bjs_format)
    # 北京时间-8小时变为格林威治时间
    utc_time = bjs_time - timedelta(hours=8)
    utc_time = utc_time.strftime(utc_format)
    return utc_time


def utc_to_bjs(utc_time):
    """
    格林时间转北京时间
    :param utc_time:
    :return:
    """
    utc_format = "%Y-%m-%dT%H:%M:%S.%f"
    bjs_format = "%Y-%m-%d %H:%M:%S"
    utc_time = datetime.strptime(utc_time, utc_format)
    # 格林威治时间+8小时变为北京时间
    bjs_time = utc_time + timedelta(hours=8)
    bjs_time = bjs_time.strftime(bjs_format)
    return bjs_time


def utc_to_gmt(utc_time, utc_fmt="%Y-%m-%d %H:%M:%S", gmt_fmt="%a %b %d %Y %H:%M:%S GMT+0800"):
    """
    UTC格式时间转GMT格式时间
    :param utc_time:
    :param utc_fmt:
    :param gmt_fmt:
    :return:
    """
    return time.strftime(gmt_fmt, time.strptime(utc_time, utc_fmt))


def gmt_utc_to(gmt_time, gmt_fmt="%a %b %d %Y %H:%M:%S GMT+0800", utc_fmt="%Y-%m-%d %H:%M:%S"):
    """
    GMT格式时间转UTC格式时间
    :param gmt_time:
    :param utc_fmt:
    :param gmt_fmt:
    :return:
    """
    return time.strftime(utc_fmt, time.strptime(gmt_time, gmt_fmt))


def get_random_str(number=6):
    """
    随机生成指定位数的字符串(a-zA-Z0-9)
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, number))


def generate_mobile():
    """
    生成随机手机号
    """
    phone = "1" + random.choice(["3", "5", "7", "8", "9"])
    for i in range(0, 9):
        num = random.randint(1, 9)
        phone += str(num)
    return phone


def month_switch(int_month):
    """
    月份转换: 数字转英文缩写
    :param int_month:
    :return:
    """
    month = "JanFebMarAprMayJunJulAugSepOctNovDec"  # 将所有月份简写存到month中
    pos = (int(int_month) - 1) * 3  # 输入的数字为n,将(n-1)*3,即为当前月份所在索引位置

    return month[pos:pos + 3]


if __name__ == '__main__':
    pass
    print(generate_mobile())
