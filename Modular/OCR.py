import requests

from SystemAPI import *

md5 = NetWorkFunc.md5
rand = NetWorkFunc.random
base64 = NetWorkFunc.base64


class BaiduOCR:
    lan = {'zh': 'CHN_ENG', 'jp': 'JAP', 'en': 'ENG', 'kor': 'KOR'}

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.ocr = HttpQuests()
        self.init()

    def init(self):
        request_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {'grant_type': 'client_credentials', 'client_id': self.api_key,
                  'client_secret': self.secret_key}
        response = requests.post(request_url, data=params)
        if response:
            try:
                self.access_token = response.json()['access_token']
            except KeyError as e:
                # Bai du OCR API get token error --- may be key error
                pass
        else:
            # usually Network error
            pass
        self.ocr.set_url('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + self.access_token)
        self.ocr.set_param('language_type', BaiduOCR.lan['jp'])
        self.ocr.set_head('content-type', 'application/x-www-form-urlencoded')

    def get_ans(self, img):
        self.ocr.set_param('image', base64(img))
        response = self.ocr.post()
        if response and 'words_result' in response.keys():
            words = str()
            for item in response['words_result']:
                words += item['words'] + '\n'
            return words
        else:
            raise ConnectionError()