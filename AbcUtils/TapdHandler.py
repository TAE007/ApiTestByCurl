# -*- coding: utf-8 -*-

import json
import requests
import base64
from TestConfig.TapdConfig import TapdConfig


class Tapd:
    # 项目id
    workSpaceId = TapdConfig.workSpaceId

    # 测试用例url根目录
    tcaseParentUrl = 'https://www.tapd.cn/%s/sparrow/tcase/view/' % workSpaceId

    # 认证字符串
    authKey = base64.b64encode(
        ':'.join([TapdConfig.apiUser, TapdConfig.apiPassword]).encode('utf-8')
    ).decode("utf-8")

    # 请求认证头信息
    header = {'Authorization': 'Basic %s' % authKey}

    @classmethod
    def getTcases(cls, **kwargs):
        try:
            # 初始化请求接口参数
            api = 'https://api.tapd.cn/tcases?workspace_id=%s&limit=200' % cls.workSpaceId

            # 组合请求参数并执行请求
            for k, v in kwargs.items():
                api = api + '&' + '='.join([k, v])
            r = requests.get(api, headers=cls.header)
            ret = r.json().get('data')

            # return
            return ret
        except:
            raise Exception('获取测试用例异常')

    @classmethod
    def getTcaseCategories(cls, **kwargs):
        # 初始化请求接口参数
        api = 'https://api.tapd.cn/tcase_categories?workspace_id=%s&limit=200' % cls.workSpaceId

        # 组合请求参数并执行请求
        for k, v in kwargs.items():
            api = api + '&' + '='.join([k, v])
        r = requests.get(api, headers=cls.header)
        ret = r.json().get('data')

        # return
        return ret


if __name__ == '__main__':
    print('debug...')

    tcases = Tapd.getTcases(category_id='1169016154001000023')
    print(json.dumps(tcases, indent=2, ensure_ascii=False))
