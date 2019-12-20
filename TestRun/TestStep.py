# -*- coding: utf-8 -*-

import time
import json
import subprocess


class TestCaseStep:
    def __init__(self, curlData):
        # Curl基础属性初始
        self.step = curlData.get('step')
        self.desc = curlData.get('desc')
        self.curl = curlData.get('curl') + ' --silent'
        self.expect = curlData.get('expect')
        self.memo = curlData.get('memo')

        # 初始化返回结果
        self.response = ''

        # 初始化用例执行相关时间统计
        self.startTime = 0
        self.endTime = 0
        self.costTime = 0

    def __setStartTime(self):
        #设置开始执行时间
        self.startTime = int(round(time.time() * 1000))

    def __setEndTime(self):
        #设置结束执行时间并同时计算出耗时
        self.endTime = int(round(time.time() * 1000))
        self.costTime = self.endTime - self.startTime

    def exec(self):
        # 设置开始执行时间
        self.__setStartTime()

        # 开始执行curl命令
        p = subprocess.Popen(self.curl, shell=True, stdout=subprocess.PIPE)
        self.response = str(p.stdout.read(), encoding='utf8')

        # 设置执行结束时间
        self.__setEndTime()


if __name__ == '__main__':
    print('debug...')
