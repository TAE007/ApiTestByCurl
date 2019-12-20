# -*- coding: utf-8 -*-

import re
import json
import time
from TestRun.TestResultChecker import Checker


class TestCase():
    def __init__(self, testCaseInfo):
        # 初始化用例基础属性信息
        self.id = testCaseInfo.get('id')
        self.module = testCaseInfo.get('module')
        self.name = testCaseInfo.get('name')
        self.preconditions = testCaseInfo.get('preconditions')
        self.steps = testCaseInfo.get('steps')
        self.expect = Checker.formatToJsonStr(testCaseInfo.get('expect'))
        self.checkType = testCaseInfo.get('checkType')
        self.url = testCaseInfo.get('url')

        # 测试用例返回结果
        self.response = ''

        # 定义归一结构化的数据
        self.expStruct = Checker.normalizeJsonStr(self.expect)
        self.resStruct = ''

        # 整个case执行时间统计
        self.startTime = 0
        self.endTime = 0
        self.costTime = 0

        # 初始化测试用例执行结果
        self.valueCheckRst = ''
        self.structCheckRst = ''

        # 所有curl请求的返回结果集合
        self.res = []

    def __setStartTime(self):
        # 设置开始执行时间
        self.startTime = int(round(time.time() * 1000))

    def __setEndTime(self):
        # 设置结束执行时间并同时计算出耗时
        self.endTime = int(round(time.time() * 1000))
        self.costTime = self.endTime - self.startTime

    def updateCurlVars(self, curl):
        try:
            vars = re.findall(r'{{(.*?)}}', curl)
            replacedCurl = curl

            for var in vars:
                varExpression = []

                ranks = var.split('.')
                varHead = ranks[0]

                # 确定是用哪一个response的返回值
                if '[' not in varHead:
                    # 如果没有下标写法，默认为上一个response的返回值
                    varExpression = ['self.res[-1]']
                else:
                    # 取次序取指定的response返回值
                    varExpression = ['self.res' + varHead.lstrip('res')]

                # 确定取返回值的哪个子值
                for rank in ranks[1:]:
                    pattern = re.compile(r'^(\w+)(\[[0-9]+\])?$')
                    match = re.match(pattern, rank)
                    varName, varIndex = match.groups()
                    varIndex = varIndex if varIndex else ''

                    varExpression.append('get(\'%s\')%s' % (varName, varIndex))

                varExpression = '.'.join(varExpression)

                # 求变量的真值
                varValue = eval(varExpression)
                replacedCurl = replacedCurl.replace('{{%s}}' % var, varValue)

            return replacedCurl
        except:
            return curl


    def runTestPreConditions(self):
        try:
            # 如果有前置条件就执行
            if self.preconditions:
                for preCondition in self.preconditions:
                    # 更新要用到上个请求返回结果的变量
                    preCondition.curl = self.updateCurlVars(preCondition.curl)
                    preCondition.exec()
                    self.res.append(json.loads(preCondition.response, encoding='utf8'))
        except Exception as e:
            print('执行前置条件时产生异常:', str(e))

    def runTestSteps(self):
        try:
            if self.steps:
                for testStep in self.steps:
                    # 更新要用到上个请求返回结果的变量
                    testStep.curl = self.updateCurlVars(testStep.curl)
                    testStep.exec()
                    stepRes = json.loads(testStep.response, encoding='utf8') if testStep.response else {}
                    self.res.append(stepRes)

                # 把测试步骤的最后一步结果作为测试用例的返回结果
                self.response = Checker.formatToJsonStr(self.steps[-1].response)
                self.resStruct = Checker.normalizeJsonStr(self.response)
            else:
                print('No steps found for testcase', self.name, self.id)
        except Exception as e:
            print('执行测试步骤时产生异常:', str(e))


    def __setTestResult(self):
        # 结构检查
        tmpStructCheckRst = Checker.check(self.checkType, self.expStruct, self.resStruct)
        self.structCheckRst = 'PASS' if tmpStructCheckRst['rst'] else 'FAIL'

        # 值检查
        tmpValCheckRst = Checker.check(self.checkType, self.expect, self.response)
        self.valueCheckRst = 'PASS' if tmpValCheckRst['rst'] else 'FAIL'
        print('测试执行结果: 结构校验=%s, 值校验=%s' % (self.structCheckRst, self.valueCheckRst))

        if self.valueCheckRst == 'FAIL':
            print('#' * 66)
            print('expect:', self.expect)
            for res in self.res:
                print('response:', res)
            print('#' * 66)

    def run(self):
        # 设置执行开始时间
        self.__setStartTime()

        # 执行前置条件
        print('测试用例名称:', self.name, self.id)
        self.runTestPreConditions()

        # 执行测试步骤
        self.runTestSteps()

        # 结果检查
        self.__setTestResult()

        # 设置执行结束时间
        self.__setEndTime()


if __name__ == '__main__':
    print('debug...')
