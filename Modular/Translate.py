from SystemAPI import *

md5 = NetWorkFunc.md5
rand = NetWorkFunc.random
base64 = NetWorkFunc.base64


class BaiduTrans:
    lan = {'zh': 'zh', 'jp': 'jp', 'en': 'en', 'kor': 'kor'}

    def __init__(self, api_id, secret_key):
        self.app_id = api_id
        self.secret_key = secret_key
        # self.init()
