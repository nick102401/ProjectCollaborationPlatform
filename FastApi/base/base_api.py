import json
import uuid

import requests
import warnings

from lxml import etree

from FastApi.common.logs_handle import Logger
from FastApi.conf import env

warnings.filterwarnings('ignore')
log = Logger().logger

header = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.107 Safari/537.36 '
}


class ApiDriver:
    """
    登录操作
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        self.login_url = 'keycloak-dev.rdev.tech/auth/realms/project/protocol/openid-connect/auth'
        self.token_url = 'keycloak-dev.rdev.tech/auth/realms/project/protocol/openid-connect/token'
        self.redirect_uri = 'https%3A%2F%2Fportal.dev.rdev.tech%2F%23%2Fmy'
        self.state = str(uuid.uuid4())
        self.nonce = str(uuid.uuid4())
        self.session = requests.Session()

    def get_login_url(self):
        """
        获取登录url及请求头cookie
        :return:
        """
        url = 'https://' + self.login_url + '?client_id=collaboration&redirect_uri=' + self.redirect_uri + \
              '&state=' + self.state + '&response_mode=fragment&response_type=code&scope=openid&nonce=' + self.nonce
        # 获取cookie并重新拼接
        response = self.session.get(url, headers=self.headers, verify=False)
        cookieList = response.headers['Set-Cookie'].split(';')
        cookieStr = ''
        for cookie in cookieList:
            if 'AUTH_SESSION_ID=' in cookie:
                cookieStr = cookie + '; '
            elif 'AUTH_SESSION_ID_LEGACY=' in cookie:
                cookieStr += cookie.replace('HttpOnly,', '').strip() + '; '
            elif 'KC_RESTART=' in cookie:
                cookieStr += cookie.replace('HttpOnly,', '').strip()
        ret_dict = {'Cookie': cookieStr}

        selector = etree.HTML(response.text)
        ret_dict['login_url'] = selector.xpath('//*[@id="kc-form-login"]')[0].attrib['action']
        return ret_dict

    def login(self):
        """
        环境登录
        :return:
        """
        ret_dict = self.get_login_url()
        # 请求头中增加cookie
        self.headers['Cookie'] = ret_dict['Cookie']

        # 登录重定向
        data = {'username': self.username,
                'password': self.password,
                'credentialId': ''}
        url = ret_dict['login_url']
        response = self.session.post(url, data=data, headers=self.headers, allow_redirects=False, verify=False)
        return response.headers

    def get_token(self):
        """
        获取token
        :return:
        """
        response = self.login()

        # 拼接cookie
        cookieList = response['set-cookie'].split('HttpOnly,')
        cookieStr = ''
        for cookie in cookieList:
            if 'KEYCLOAK_IDENTITY=' in cookie:
                cookieStr = cookie.split('Version=1')[0]
            elif 'KEYCLOAK_IDENTITY_LEGACY=' in cookie:
                cookieStr += cookie.split('Version=1')[0]
            elif 'KEYCLOAK_SESSION=' in cookie:
                cookieStr += cookie.split('Version=1')[0]
                cookieStr += cookie.split('Version=1')[0].replace(';', '').replace('KEYCLOAK_SESSION',
                                                                                   'KEYCLOAK_SESSION_LEGACY', 1)

        self.headers['Cookie'] = self.headers['Cookie'].split('KC_RESTART=')[0] + cookieStr
        self.headers['Content-type'] = 'application/x-www-form-urlencoded'

        # 获取参数
        location = response['location']
        code = location.split('code=')[1]
        redirect_uri = location.split('&')[0]

        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': 'collaboration',
            'redirect_uri': redirect_uri,
        }
        url = 'https://' + self.token_url

        response = self.session.post(url, data=data, headers=self.headers, verify=False)
        return dict({'content': response.text, 'retCode': response.status_code})

    def get(self, url, headers=None):
        response = self.session.get(url=url, headers=headers, verify=False)
        return dict({'content': json.loads(response.text), 'retCode': response.status_code})

    def post(self, url, data, files, headers=None):
        response = self.session.post(url=url, data=data, files=files, headers=headers, verify=False)
        return dict({'content': json.loads(response.text), 'retCode': response.status_code})

    def patch(self, url, data, headers=None):
        response = self.session.patch(url=url, data=data, headers=headers, verify=False)
        return dict({'content': json.loads(response.text), 'retCode': response.status_code})

    def put(self, url, data, headers=None):
        response = self.session.put(url=url, data=data, headers=headers, verify=False)
        return dict({'content': json.loads(response.text), 'retCode': response.status_code})

    def delete(self, url, data, headers=None):
        response = self.session.delete(url=url, data=data, headers=headers, verify=False)
        return dict({'content': json.loads(response.text), 'retCode': response.status_code})


def req_exec(method, url, data=None, files=None, headers=None, username=env.USERNAME, password=env.PASSWORD):
    """
    接口执行
    :param method: 接口请求方式
    :param url: 接口url
    :param data: 接口入参
    :param files: 文件参数
    :param headers: 接口请求头
    :param username: 登录账号
    :param password: 登录密码
    :return:
    """
    # 获取token
    api_driver = ApiDriver(username=username, password=password)
    header['Authorization'] = 'Bearer ' + json.loads(api_driver.get_token()['content'])['access_token']
    header['user'] = username

    # 默认请求头参数
    if headers:
        for k, v in headers.items():
            header[k] = v
    headers = header

    # url拼接
    if not url.startswith('/'):
        url = '/' + url
    url = 'https://' + env.HOST + url

    print_data = data
    if data:
        data = json.dumps(data)
    # 默认返回
    response = None
    if method == 'GET':
        response = api_driver.get(url, headers=headers)
    elif method == 'POST':
        response = api_driver.post(url, data, files, headers=headers)
    elif method == 'PATCH':
        response = api_driver.patch(url, data, headers=headers)
    elif method == 'PUT':
        response = api_driver.put(url, data, headers=headers)
    elif method == 'DELETE':
        response = api_driver.delete(url, data, headers=headers)

    # 日志打印
    log.info('[' + method + ']:' + url)
    if method != 'GET':
        log.info(
            '[DATA]:\n' + json.dumps(print_data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    log.info('[RESP]:' + str(response))
    return response


if __name__ == '__main__':
    driver = ApiDriver(env.USERNAME, env.PASSWORD)
    # print(driver.login_url())
    print(driver.get_token())
    # print(is_login())
    # data = {
    #     "title": "test12345",
    #     "pid": 138445528022784,
    #     "priority": "1",
    #     "workType": "task",
    #     "remark": "",
    #     "estimatedBegintime": "2021-08-17",
    #     "estimatedEndtime": "",
    #     "estimatedWorkhour": "",
    #     "progress": 0,
    #     "createPerson": "huixiaoying",
    #     "status": "notstart"
    # }
    # resp = req_exec(method='POST',
    #                 url='/api/project/updateProjecItem',
    #                 data=data)
    # print(json.loads(resp['content'])['data']['token'])
