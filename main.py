import base64
import json
from io import BytesIO

import requests

from WinAPI import *
import tkinter as tk
from functools import reduce

hotKey = HotKey()
screen = ScreenCut()
translate = HTTP()
mainWin = tk.Tk()
mainWin.wm_attributes('-topmost', 1)
mainWin.geometry('1000x100+300+300')
access_token = ""
ans_label = tk.Text(mainWin, background="#ccc")
ans_label.pack()
appid = ""
secretKey = ""


def add_node():
    print("add")
    screen.add_mouse_point()


def quit_app():
    hotKey.stop()
    translate.close()
    exit(0)


def clear():
    screen.clear()


def trans():
    img = screen.cut()
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    params = {"image": base64_str, 'language_type': 'JAP'}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        words = ""
        if 'words_result' in response.json().keys():
            for item in response.json()['words_result']:
                words += item['words'] + '\n'
        salt = translate.random(32768, 65536)
        sign = translate.md5(appid + words + str(salt) + secretKey)
        translate.add_param('salt', salt)
        translate.add_param('sign', sign)
        translate.add_param('q', words)
        res = translate.get()
        print(res)
        ans = ""
        if 'trans_result' in res.keys():
            for item in res['trans_result']:
                ans += item['dst'] + '\n'
        global ans_label
        ans_label.delete(1.0, tk.END)
        ans_label.insert(tk.END, "Src: " + words + "\nTra: " + ans)


def api_init():
    f = open('setting.json')
    id = json.load(f)
    f.close()
    global appid
    appid = id['translate']['appid']
    global secretKey
    secretKey = id['translate']['secretKey']

    request_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {'grant_type': 'client_credentials', 'client_id': id['OCR']['apiKey'],
              'client_secret': id['OCR']['SecretKey']}
    response = requests.post(request_url, data=params)
    if response:
        global access_token
        access_token = response.json()['access_token']

    translate.set_host('api.fanyi.baidu.com')
    translate.set_url('/api/trans/vip/translate')
    translate.connect()
    translate.add_param('appid', appid)
    translate.add_param('secretKey', secretKey)
    translate.add_param('from', 'auto')
    translate.add_param('to', 'zh')


def hot_key_init():
    hotKey.add_key("AddNode", (0, 'a'), add_node)
    hotKey.add_key("clear", (0, 'c'), clear)
    hotKey.add_key("ESC", (0, KeyCode.ESCAPE), quit_app)
    hotKey.add_key("Translate", (0, 't'), trans)
    hotKey.start()


hot_key_init()
api_init()

mainWin.mainloop()
quit_app()
