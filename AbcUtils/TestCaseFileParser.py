# -*- coding: utf-8 -*-

import re
import json
import html
from AbcUtils.TapdHandler import Tapd
from TestConfig.TapdConfig import TapdConfig


class TestCaseParser:
    # 初始化设置测试用例目录名称和id
    apiTestCategoryName = TapdConfig.apiTcaseRootDirName
    allCategories = []
    apiTestCategoryId = ''
    apiTestModules = []

    @classmethod
    def setRootCategoryId(cls):
        # 设置api接口用例目录的id
        if not cls.apiTestCategoryId:
            categories = Tapd.getTcaseCategories()
            cls.allCategories = categories
            for categoryInfo in categories:
                if categoryInfo.get('TcaseCategory').get('name') == cls.apiTestCategoryName:
                    cls.apiTestCategoryId = categoryInfo.get('TcaseCategory').get('id')
                    break

            print('API接口测试用例根目录信息: name:%s, id:%s' % (cls.apiTestCategoryName, cls.apiTestCategoryId))

    @classmethod
    def getRootParentCategoryId(cls, categoryId):
        # 设置根目录id
        cls.setRootCategoryId()

        ret = ''
        for categoryInfo in cls.allCategories:
            id = categoryInfo.get('TcaseCategory').get('id')
            pid = categoryInfo.get('TcaseCategory').get('parent_id')
            if id == categoryId:
                if pid == '0':
                    ret = id
                    break
                else:
                    ret = cls.getRootParentCategoryId(pid)
                    break

        return ret

    @classmethod
    def getTestModules(cls, **kwargs):
        cls.setRootCategoryId()

        for categoryInfo in cls.allCategories:
            id = categoryInfo.get('TcaseCategory').get('id')
            name = categoryInfo.get('TcaseCategory').get('name')

            # 获取根目录id
            rootCategoryId = cls.getRootParentCategoryId(id)
            if rootCategoryId == cls.apiTestCategoryId:
                if id != cls.apiTestCategoryId:
                    cls.apiTestModules.append({'id': id, 'name': name})

        return cls.apiTestModules

    @classmethod
    def getCheckType(cls, tcaseInfo):
        checkType = 'resContainsExpect'

        checkTypes = [
            'resContainsExpect',
            'resNotContainsExpect',
            'resEqualExpect',
            'resNotEqualExpect'
        ]

        for i in range(50, 0, -1):
            val = tcaseInfo.get('Tcase').get('custom_field_%d' % i)
            if val in checkTypes:
                checkType = val
                break

        return checkType

    @classmethod
    def checkCurlValidation(cls, caseInfo):
        # 初始化变量定义
        allVars = []

        # 先找前置条件中的变量定义
        preconditionCurlsStr = caseInfo.get('Tcase').get('precondition')
        if preconditionCurlsStr:
            allVars = re.findall(r'{{(res.*?)}}', preconditionCurlsStr)

        # 再找测试步骤中的变量定义
        testStepCurlsStr = caseInfo.get('Tcase').get('steps')
        if testStepCurlsStr:
            allVars += re.findall(r'{{(res.*?)}}', testStepCurlsStr)

        # 检查变量的写法是否规范
        pattern = re.compile(r'^res(\d+)?(\.\S+)*$')
        for var in allVars:
            if not re.match(pattern, var):
                raise Exception('可变参数表示格式错误，请检查:', var)

    @classmethod
    def getModuleTestCases(cls, moduleInfo, **kwargs):
        # 获取tapd对应模块的用例data
        tcases = Tapd.getTcases(category_id=moduleInfo.get('id'))

        testcases = []
        for tcase in tcases:
            # 对可变参数进行格式校验
            cls.checkCurlValidation(tcase)

            # 处理执行步骤data
            stepsData = []
            srcSteps = tcase.get('Tcase').get('steps').replace('\n', '')
            steps = re.findall(r'【(.*?)】', srcSteps)

            if srcSteps and not steps:
                print('没有匹配到测试步骤:', srcSteps)

            for idx, step in enumerate(steps):
                stepsData.append({
                    'step': idx,
                    'desc': '',
                    'curl': html.unescape(step.strip()),
                    'expect': '',
                    'memo': ''
                })

            # 处理前置条件data
            preConditionData = []
            preconditionStr = tcase.get('Tcase').get('precondition')
            if preconditionStr:
                preConditions = re.findall(r'【(.*?)】', preconditionStr)

                if preconditionStr and not preConditions:
                    print('没有匹配到前置条件:', preconditionStr)

                for idx, preCondition in enumerate(preConditions):
                    preConditionData.append({
                        'step': idx,
                        'desc': '',
                        'curl': html.unescape(preCondition.strip()),
                        'expect': '',
                        'memo': ''
                    })

            # 处理测试用例data
            caseData = {
                'module': moduleInfo.get('name'),
                'id': tcase.get('Tcase').get('id')[-7:],
                'name': tcase.get('Tcase').get('name'),
                'preconditions': preConditionData,
                'steps': stepsData,
                'expect': tcase.get('Tcase').get('expectation'),
                'checkType': cls.getCheckType(tcase),
                'url': Tapd.tcaseParentUrl + tcase.get('Tcase').get('id')
            }

            testcases.append(caseData)

        # 返回用例数据
        print('模块: %s, 用例数: %d' % (moduleInfo.get('name'), len(testcases)))
        return testcases


if __name__ == '__main__':
    print('debug...')

    testModules = TestCaseParser.getTestModules()
    print(json.dumps(testModules, indent=2, ensure_ascii=False))

    mInfo = {
        "id": "1169016154001000023",
        "name": "租赁概览"
    }
    tcases = TestCaseParser.getModuleTestCases(mInfo)
    print('tcases:', json.dumps(tcases, indent=2, ensure_ascii=False))
