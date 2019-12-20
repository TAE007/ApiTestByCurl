# -*- coding: utf-8 -*-

import os
import difflib
from jinja2 import Environment, FileSystemLoader
from TestRun.TestResultChecker import Checker


class ReportWriter:
    #define report directory
    reportDir = os.path.join(os.path.dirname(__file__), '../TestReport')
    diffDir = os.path.join(reportDir, 'Diff')

    # define the template report file.
    templateReport = os.path.abspath(os.path.join(os.path.dirname(__file__), '../TestConfig/TemplateReport.html'))
    templateDiff = os.path.abspath(os.path.join(os.path.dirname(__file__), '../TestConfig/TemplateDiff.html'))

    #定义报告文件名称
    reportFileName = 'ApiAutoTestReport.html'

    @classmethod
    def getReportHtmlFileName(cls):
        #组合报告文件路径，并删除旧的报告文件
        reportFile = os.path.join(cls.reportDir, cls.reportFileName)
        return reportFile

    @classmethod
    def getDiffHtmlFileName(cls, caseId):
        #组合diff报告文件路径
        diffFile = os.path.join(cls.diffDir, caseId + '.html')
        return diffFile

    @classmethod
    def clearOldReportFiles(cls):
        print('清除旧的测试报告文件')
        if not os.path.exists(cls.reportDir):
            os.mkdir(cls.reportDir)
        else:
            #删除旧的报告文件
            reportFile = cls.getReportHtmlFileName()
            if os.path.exists(reportFile):
                os.remove(reportFile)

            #删除旧的diff报告文件
            if not os.path.exists(cls.diffDir):
                os.mkdir(cls.diffDir)
            else:
                for f in os.listdir(cls.diffDir):
                    os.remove(os.path.join(cls.diffDir, f))

    @classmethod
    def generateReportHtml(cls, allTestCaseRunRst):
        allCases = 0
        passNumber = 0
        failNumber = 0
        totalCostTime = 0
        for module in allTestCaseRunRst:
            moduleCasesRst = allTestCaseRunRst.get(module)

            for caseRst in moduleCasesRst:
                if caseRst.valueCheckRst == 'PASS':
                    passNumber += 1
                else:
                    failNumber += 1

                totalCostTime += caseRst.costTime
                allCases += 1

        env = Environment(loader=FileSystemLoader(os.path.dirname(cls.templateReport)))
        template = env.get_template(os.path.basename(cls.templateReport))
        with open(cls.getReportHtmlFileName(), 'w+', encoding='utf8') as htmlWriter:
            htmlContent = template.render(
                allTestCaseRunRst = allTestCaseRunRst,
                totalModule = allCases,
                passNumber = passNumber,
                failNumber = failNumber,
                totalCostTime = totalCostTime,
            )
            htmlWriter.write(htmlContent)

    @classmethod
    def diffJsonStr(cls, expJsonStr, resJsonStr, fromdesc, todesc):
        differ = difflib.HtmlDiff()
        return differ.make_table(
            expJsonStr.splitlines(),
            resJsonStr.splitlines(),
            fromdesc = fromdesc,
            todesc= todesc
        )

    @classmethod
    def generateDiffHtml(cls, testcaseRunRst):
        #获取html文件名称
        caseId = testcaseRunRst.id
        caseName = testcaseRunRst.name
        expStruct = Checker.formatToJsonStr(testcaseRunRst.expStruct, indent=2)
        resStruct = Checker.formatToJsonStr(testcaseRunRst.resStruct, indent=2)
        expValue = Checker.formatToJsonStr(testcaseRunRst.expect, indent=2)
        resValue = Checker.formatToJsonStr(testcaseRunRst.response, indent=2)
        testResult = testcaseRunRst.valueCheckRst

        diffHtml = cls.getDiffHtmlFileName(caseId)

        env = Environment(loader=FileSystemLoader(os.path.dirname(cls.templateDiff)))
        template = env.get_template(os.path.basename(cls.templateDiff))
        with open(diffHtml, 'w+', encoding='utf8') as htmlWriter:
            htmlContent = template.render(
                structDiffResult = cls.diffJsonStr(expStruct, resStruct, fromdesc='期望返回结构', todesc='实际返回结构'),
                valueDiffResult = cls.diffJsonStr(expValue, resValue, fromdesc='期望返回值', todesc='实际返回值'),
                caseId = caseId,
                caseDesc = caseName,
                testRst = testResult
            )
            htmlWriter.write(htmlContent)


if __name__ == '__main__':
    print('debug...')

