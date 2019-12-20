# -*- coding: utf-8 -*-

import datetime


def getCurrentDate(**kwargs):
    # 先获取当前日期，格式：2019/06/01
    crtDate = datetime.datetime.now()

    formater = kwargs.get('format', '%d/%d/%d')
    crtDate = formater % (crtDate.year, crtDate.month, crtDate.day)
    return crtDate


def getLastDate(**kwargs):
    # 参数处理，默认为明天
    day = kwargs.get('day', 1)

    # 计算未来日期
    futureDate = datetime.datetime.now() - datetime.timedelta(days=day)
    formater = kwargs.get('format', '%d/%d/%d')
    futureDate = formater % (futureDate.year, futureDate.month, futureDate.day)
    return futureDate


def getFutureDate(**kwargs):
    # 参数处理，默认为明天
    day = kwargs.get('day', 1)

    # 计算未来日期
    futureDate = datetime.datetime.now() + datetime.timedelta(days=day)
    formater = kwargs.get('format', '%d/%d/%d')
    futureDate = formater % (futureDate.year, futureDate.month, futureDate.day)

    print('未来(%d天)日期：%s' % (day, futureDate))

    return futureDate


if __name__ == '__main__':
    print('debug...')
