# -*- coding: utf-8 -*-

import re
import json
import sys

sys.setrecursionlimit(1500)


class Checker:
    @classmethod
    def formatToJsonStr(cls, dataStr, **kwargs):
        newDataStr = dataStr.strip()

        try:
            dataJson = json.loads(newDataStr, encoding='utf8')
            if 'indent' in kwargs:
                return json.dumps(
                    dataJson,
                    indent=kwargs.get('indent'),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(',', ':')
                )
            else:
                return json.dumps(
                    dataJson,
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(',', ':')
                )
        except:
            try:
                #尝试加大括号再转换
                newDataStr = '{%s}' % newDataStr
                dataJson = json.loads(newDataStr, encoding='utf8')
                if 'indent' in kwargs:
                    return json.dumps(
                        dataJson,
                        indent=kwargs.get('indent'),
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(',',':')
                    ).lstrip('{').rstrip('}')
                else:
                    return json.dumps(
                        dataJson,
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(',',':')
                    ).lstrip('{').rstrip('}')
            except:
                try:
                    #尝试加中括号再转换
                    newDataStr = '[%s]' % newDataStr
                    dataJson = json.load(newDataStr, encoding='utf8')
                    if 'indent' in kwargs:
                        return json.dumps(
                            dataJson,
                            indent=kwargs.get('indent'),
                            sort_keys=True,
                            ensure_ascii=False,
                            separators=(',',':')
                        ).lstrip('[').rstrip(']')
                    else:
                        return json.dumps(
                            dataJson,
                            sort_keys=True,
                            ensure_ascii=False,
                            separators=(',',':')
                        ).lstrip('[').rstrip(']')
                except Exception as e:
                    print('格式化为json字符串时产生异常:', str(e))
                    # print('dataStr:', newDataStr)
                    return newDataStr

    @classmethod
    def normalizeJsonStr(cls, jsonStr):
        try:
            #执行json格式化
            formatedJsonStr = cls.formatToJsonStr(jsonStr)

            # 归一化：字符串
            finalStr = re.sub(r':".*?"', ':"{string}"', formatedJsonStr)

            # 归一化：年-月-日
            finalStr = re.sub(r'\d+-\d+-\d+', ':"{date}"', finalStr)

            # 归一化：时：分：秒
            finalStr = re.sub(r'\d+:\d+:\d+(\.\d+)?', '"{time}"', finalStr)

            # 归一化：小数
            finalStr = re.sub(r':\d+\.\d+', ':"{number}"', finalStr)

            # 归一化：整数
            finalStr = re.sub(r':\d+', ':"{number}"', finalStr)

            # 归一化：boolean
            finalStr = re.sub(r':(false|true)', ':"{boolean}"', finalStr)

            return finalStr
        except Exception as e:
            print('str转json并归一化的过程中出现异常:', str(e))
            return jsonStr

    @classmethod
    def resContainsExpect(cls, expect, response):
        if expect in response:
            return {'rst': True, 'msg': ''}
        else:
            return {'rst': False, 'msg': 'res不包含exp'}

    @classmethod
    def resNotContainsExpect(cls, expect, response):
        if cls.resContainsExpect(expect, response).get('rst'):
            return {'rst': False, 'msg': 'res中包含exp'}
        else:
            return {'rst': True, 'msg': ''}

    @classmethod
    def resEqualExpect(cls, expect, response):
        if expect == response:
            return {'rst': True, 'msg': ''}
        else:
            return {'rst': False, 'msg': 'res不等于exp'}

    @classmethod
    def resNotEqualExpect(cls, expect, response):
        if cls.resEqualExpect(expect, response):
            return {'rst': False, 'msg': 'res等于exp'}
        else:
            return {'rst': True, 'msg': ''}

    @classmethod
    def check(cls, checkType, expect, response):
        if checkType == 'resContainsExpect':
            return cls.resContainsExpect(expect, response)
        elif checkType == 'resNotContainsExpect':
            return cls.resNotContainsExpect(expect, response)
        elif checkType == 'resEqualExpect':
            return cls.resEqualExpect(expect, response)
        elif checkType == 'resNotEqualExpect':
            return cls.resNotEqualExpect(expect, response)
        else:
            raise Exception('不支持的测试结果校验类型:', checkType)


if __name__ == '__main__':
    print('debug...')
