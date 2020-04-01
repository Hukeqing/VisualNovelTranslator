from SystemAPI import *


class BaiduTrans:
    lan = {'zh': 'zh', 'jp': 'jp', 'en': 'en', 'kor': 'kor'}

    def __init__(self, api_id, secret_key):
        self.app_id = api_id
        self.secret_key = secret_key
        self.translate = HttpClient()
        self.salt = NetWorkFunc.random(32768, 65536)
        self.from_lan = 'jp'
        self.to_lan = 'zh'
        self.init()

    def init(self):
        self.translate.set_host('api.fanyi.baidu.com')
        self.translate.set_url('/api/trans/vip/translate')
        self.translate.connect()
        self.translate.add_param('appid', self.app_id)
        self.translate.add_param('secretKey', self.secret_key)
        self.translate.add_param('from', BaiduTrans.lan[self.from_lan])
        self.translate.add_param('to', BaiduTrans.lan[self.to_lan])
        self.translate.add_param('salt', self.salt)

    def get_ans(self, words):
        sign = NetWorkFunc.md5(self.app_id + words + str(self.salt) + self.secret_key)
        self.translate.add_param('sign', sign)
        self.translate.add_param('q', words)
        res = self.translate.get()
        ans = "百度: "
        try:
            if 'trans_result' in res.keys():
                for item in res['trans_result']:
                    ans += item['dst'] + '\n'
        except Exception as e:
            print(e)
            print(res)
            ans += '<ERROR>'
        return ans

    def set_from_lan(self, lan):
        self.from_lan = lan
        self.translate.add_param('from', BaiduTrans.lan[self.from_lan])

    def set_to_lan(self, lan):
        self.to_lan = lan
        self.translate.add_param('to', BaiduTrans.lan[self.to_lan])

    def close(self):
        self.translate.close()


trans_api_dict = {'baidu': BaiduTrans}
