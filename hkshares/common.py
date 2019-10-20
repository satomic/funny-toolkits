# coding=utf-8

import datetime


def current_time(fmt='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.datetime.now().strftime(fmt)

def date_add_day(date_origin_str, day=0):
    '''
    :param date_origin_str: 只支持 2012-03-05 格式
    :param day: 数字
    :return: 
    '''
    date_origin = datetime.datetime.strptime(date_origin_str, '%Y-%m-%d')
    delta = datetime.timedelta(days=day)
    date_new = date_origin + delta
    return date_new.strftime('%Y-%m-%d')


def print_base(base_info, type):
    print("%s [%s] %s" % (current_time(), type, base_info))


def print_err(err, type="ERRO"):
    print_base(err, type)


def print_info(info, type="INFO"):
    print_base(info, type)


def print_warn(warn, type="WARN"):
    print_base(warn, type)


if __name__ == "__main__":
    print(current_time())
    print(date_add_day("2013-01-01", -1))
    print_info("这是一条信息")
    print_warn("这是一条告警")
    print_err("这是一条错误")