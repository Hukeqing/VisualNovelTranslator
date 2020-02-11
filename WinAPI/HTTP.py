# coding=utf-8
import hashlib
import http.client
import json
import random
import urllib.parse


class HTTP:
    @staticmethod
    def md5(value):
        return hashlib.md5(value.encode()).hexdigest()

    @staticmethod
    def random(min_value, max_value):
        return random.randint(min_value, max_value)

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


def test_http():
    f = open('../setting.json', 'r')
    data = json.load(f)
    appid = data['translate']['appid']
    secretKey = data['translate']['secretKey']
    h = HTTP()
    h.set_host('api.fanyi.baidu.com')
    h.set_url('/api/trans/vip/translate')
    param = {'appid': appid, 'q': input(), 'from': 'auto', 'to': 'zh', 'salt': h.random(32768, 65536)}
    sign = h.md5(appid + param['q'] + str(param['salt']) + secretKey)
    param['sign'] = sign
    h.set_param(param)
    h.connect()
    print(h.get())


if __name__ == '__main__':
    test_http()
