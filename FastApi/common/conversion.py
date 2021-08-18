# in_dict:需要处理的字典, target_key:目标键
# value:输出的列表,元素为目标键值对应的值(必须为空列表), not_ldt:获取的目标类型不为dict

import requests

from FastApi.base.base_api import ApiDriver
from FastApi.common.logs_handle import Logger
from FastApi.conf import env

log = Logger().logger
dicts = {'1': 1, '2': 2, '3': 3, '4': {'5': 55, '6': 66, '7': 77}, '7': {'7': 777}}


class A(object):
    def __init__(self):
        self.b = B


class B(object):
    def __init__(self):
        self.a = A


def get_color():
    url = 'https://blog.csdn.net/qq_27918787/article/details/52744450'
    resp = requests.get(url)
    print(resp.content)


def fun_a(**params):
    for param in params.keys():
        print(param)


if __name__ == '__main__':
    pass
    # param = 'Department head'
    # print(param.upper())
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    # print(bjs_to_utc(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    #
    # print(chardet.detect(str.encode('中文项目')))

    # int_a = 0
    # if int_a is not None:
    #     print(True)

    # b = B()
    #
    # str_a = 'Thu Aug 05 2021 00:00:00 GMT+0800'
    # print(str_a.replace('00:00:00', '08:00:00'))
    # print(str_a)

    # xxx = '{"valid": True, "tempId": "ST-72f987fe9f8646618c9ca66fc63c3135", "description": "", "endTime": "2021-08-06", "startTime": "2021-08-05"}'
    # x_list = ast.literal_eval(xxx)
    # print(type(x_list))

    # get_color()

    # api_driver = ApiDriver(username=env.USERNAME_PM, password=env.USER_PWD)
    # token = api_driver.get_token()
    #
    # data = {
    #     "allOnly": False,
    #     "createrOnly": True,
    #     "desc": '',
    #     "fileName": 'Jenkins流水线配置.docx',
    #     "projectOnly": False,
    #     "title": 'Jenkins流水线配置.docx'
    # }
    # files = {'file': ('Jenkins流水线配置.docx', open('../../../temp/TaskForce1/FastApi/data/Jenkins流水线配置.docx', 'rb'), 'application/*')}
    # url = 'http://172.30.1.21:10090/api/task/case/task/P-e89ce786c70842d6b1e2a299cace16e5/upload'
    # header = {
    #     'Accept': 'application/json, text/plain, */*',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Connection': 'keep-alive',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/92.0.4515.107 Safari/537.36 ',
    #     'token': token
    # }
    #
    # resp = requests.post(url=url, data=data, files=files, headers=header)
    # print(resp.text)

    # print(float(520))

    # fun_a()

    # float_a = 60.0
    # print(int(float_a))

    print(3781/10400)
    print(8/21.75)
