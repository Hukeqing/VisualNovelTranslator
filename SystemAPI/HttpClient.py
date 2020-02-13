# coding=utf-8
import base64
import hashlib
import http.client
import json
import random
import urllib.parse
from io import BytesIO

import requests


class NetWorkFunc:
    @staticmethod
    def md5(value):
        return hashlib.md5(value.encode()).hexdigest()

    @staticmethod
    def random(min_value, max_value):
        return random.randint(min_value, max_value)

    @staticmethod
    def base64(img):
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        byte_data = img_buffer.getvalue()
        return base64.b64encode(byte_data)


class HttpClient:
    def __init__(self):
        self.host = None
        self.url = None
        self.param = dict()
        self.httpClient = None

    def set_host(self, host):
        self.host = host

    def set_url(self, url):
        self.url = url

    def add_param(self, key, value):
        self.param[key] = value

    def set_param(self, parm: dict):
        self.param = parm

    def clear_param(self):
        self.param.clear()

    def connect(self):
        try:
            self.httpClient = http.client.HTTPConnection(self.host)
        except Exception as e:
            print(e)

    def get(self, encode='utf-8'):
        if self.httpClient is None:
            self.connect()
        flag = False
        url = self.url
        for key, value in self.param.items():
            url += '&' if flag else '?'
            url += str(key) + '=' + urllib.parse.quote(str(value))
            flag = True
        try:
            self.httpClient.request('GET', url)
            response = self.httpClient.getresponse()
            result_all = response.read().decode(encode)
            return json.loads(result_all)
        except Exception as e:
            print('Fail in Get', e)

    def close(self):
        if self.httpClient:
            self.httpClient.close()


class HttpQuests:
    def __init__(self):
        self.params = dict()
        self.headers = dict()
        self.url = ""

    def set_param(self, key, value):
        self.params[key] = value

    def set_head(self, key, value):
        self.headers[key] = value

    def set_url(self, url):
        self.url = url

    def post(self):
        response = requests.post(self.url, data=self.params, headers=self.headers)
        if response:
            return response.json()
        return None


def test_http():
    f = open('../setting.json', 'r')
    data = json.load(f)
    appid = data['translate']['appid']
    secretKey = data['translate']['secretKey']
    h = HttpClient()
    h.set_host('api.fanyi.baidu.com')
    h.set_url('/api/trans/vip/translate')
    param = {'appid': appid, 'q': input(), 'from': 'auto', 'to': 'zh', 'salt': NetWorkFunc.random(32768, 65536)}
    sign = NetWorkFunc.md5(appid + param['q'] + str(param['salt']) + secretKey)
    param['sign'] = sign
    h.set_param(param)
    h.connect()
    print(h.get())


if __name__ == '__main__':
    test_http()
