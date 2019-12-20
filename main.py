# -*- coding: utf-8 -*-

import os
import sys

from AbcUtils.TestCaseFileParser import TestCaseParser
from TestRun.TestCaseInfo import TestCase
from TestRun.TestStep import TestCaseStep
from TestRun.TestPreCondition import TestPreCondition
from AbcUtils.ReportWriter import ReportWriter


def main(**kwargs):
    #清除旧的报告文件
    ReportWriter.clearOldReportFiles()

    # 从excel表格中取出模块
    testModulesInfo = TestCaseParser.getTestModules()

    # 判断是否debug模式
    debugCaseId = kwargs.get('caseId', None)

    # 以模块为单位，取出模块的测试用例
    allTestCaseRunRst = {}
    for moduleInfo in testModulesInfo:
        moduleName = moduleInfo.get('name')

        if not debugCaseId:
            moduleTestCasesInfo = TestCaseParser.getModuleTestCases(moduleInfo)
        else:
            moduleTestCasesInfo = [ci for ci in TestCaseParser.getModuleTestCases(moduleInfo) if
                                   debugCaseId == ci.get('id')]

        if not moduleTestCasesInfo:
            continue

        # 转换为用例执行对象
        allTestCaseRunRst[moduleName] = []
        for testCaseInfo in moduleTestCasesInfo:
            # 实例化测试步骤对象
            stepObjs = [TestCaseStep(stepData) for stepData in testCaseInfo.get('steps')]
            preconditionObjs = [TestPreCondition(preConditionData) for preConditionData in
                                testCaseInfo.get('preconditions')]

            # 实例化测试用例对象
            testCaseObj = TestCase({
                'id': testCaseInfo.get('id'),
                'module': testCaseInfo.get('module'),
                'name': testCaseInfo.get('name'),
                'preconditions': preconditionObjs,
                'steps': stepObjs,
                'expect': testCaseInfo.get('expect'),
                'checkType': testCaseInfo.get('checkType'),
                'url': testCaseInfo.get('url')
            })

            # 执行测试用例
            testCaseObj.run()

            ReportWriter.generateDiffHtml(testCaseObj)

            allTestCaseRunRst[moduleName].append(testCaseObj)

    # Generate html report.
    ReportWriter.generateReportHtml(allTestCaseRunRst)


if __name__ == '__main__':
    # 获取环境变量参数
    debugCaseId = os.getenv('DEBUG_CASE_ID')

    # 根据构建时传入的参数觉得是调试模式还是测试执行模式
    if debugCaseId == 'all':
        main()
    else:
        main(caseId=debugCaseId)
        # main(caseId='1000093')

    sys.exit(0)
