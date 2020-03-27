import json
import time
import tkinter as tk
import tkinter.ttk

from PIL import ImageTk

from Modular import OCR
from SystemAPI import *

screen = ScreenCut()
translate = HttpClient()
# ocr = HttpQuests()

lan = {'中文': ('CHN_ENG', 'zh'), '日语': ('JAP', 'jp'), '英语': ('ENG', 'en'), '韩语': ('KOR', 'kor')}

mainWin = tk.Tk()
mainWin.title('Visual Novel Translator')
# mainWin.configure(background='red')
mainWin.wm_attributes('-topmost', 1)
mainWin.wm_attributes("-alpha", 0.8)
mainWin.geometry('1000x150+300+300')

ans_label = tk.Label(mainWin, background="#cccccc", font=('Microsoft YaHei', 10))
ans_label.place(relx=0.5, rely=0.5, anchor='center', width=400, height=125)
# ans_label.config(state='disabled')

menubar = tk.Menu(mainWin)
mainWin.config(menu=menubar)

log_variable = tk.StringVar()

appid = ""
secretKey = ""
fromLag = ""

baiduOCR: OCR.BaiduOCR


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            log_variable.set(time.strftime("%M:%S", time.localtime()) + ' ' + text + '\n' + log_variable.get())
            # log_label.insert(1.0, time.strftime("%M:%S", time.localtime()) + ' ' + text + '\n')
            return func(*args, **kw)

        return wrapper

    return decorator


@log('From Changed')
def change_from(x):
    cur = lan[fromString.get()]
    # ocr.set_param('language_type', cur[0])
    translate.add_param('from', cur[1])


@log('To Changed')
def change_to(x):
    cur = lan[toString.get()]
    translate.add_param('to', cur[1])


fromString = tk.StringVar()
fromCombobox = tk.ttk.Combobox(mainWin, textvariable=fromString, width=10)
fromCombobox['value'] = tuple(lan.keys())
fromCombobox.current(1)
fromCombobox.bind("<<ComboboxSelected>>", change_from)
fromCombobox.place(relx=0.5, rely=0.5, anchor='center', x=-400, y=-30)

toString = tk.StringVar()
toCombobox = tk.ttk.Combobox(mainWin, textvariable=toString, width=10)
toCombobox['value'] = tuple(lan.keys())
toCombobox.current(0)
toCombobox.bind("<<ComboboxSelected>>", change_to)
toCombobox.place(relx=0.5, rely=0.5, anchor='center', x=-400, y=30)


def quit_app():
    mainWin.quit()
    translate.close()
    exit(0)


@log('Clear')
def clear():
    print("clear")
    screen.clear()


@log('Show')
def show():
    print("show")
    screen.show_region()


@log('Translate')
def trans():
    img = screen.cut()

    # ocr.set_param('image', NetWorkFunc.base64(img))
    # response = ocr.post()
    words = baiduOCR.get_ans(img)
    # if response is not None and 'words_result' in response.keys():
    #     print(response)
    #     for item in response['words_result']:
    #         words += item['words'] + '\n'
    if words == "":
        ans_label.config(text='Distinguish No Words!')
        return
    salt = NetWorkFunc.random(32768, 65536)
    sign = NetWorkFunc.md5(appid + words + str(salt) + secretKey)
    translate.add_param('salt', salt)
    translate.add_param('sign', sign)
    translate.add_param('q', words)
    res = translate.get()
    ans = ""
    if 'trans_result' in res.keys():
        for item in res['trans_result']:
            ans += item['dst'] + '\n'
    ans_label.config(text='原文: ' + words + '\n百度翻译: ' + ans)
    # print('原文: ' + words + '\n百度翻译: ' + ans)


def api_init():
    f = open('setting.json')
    id = json.load(f)
    f.close()
    global appid
    appid = id['translate']['appid']
    global secretKey
    secretKey = id['translate']['secretKey']
    global baiduOCR
    baiduOCR = OCR.BaiduOCR(id['OCR']['apiKey'], id['OCR']['SecretKey'])
    # request_url = "https://aip.baidubce.com/oauth/2.0/token"
    # params = {'grant_type': 'client_credentials', 'client_id': id['OCR']['apiKey'],
    #           'client_secret': id['OCR']['SecretKey']}
    # response = requests.post(request_url, data=params)
    # access_token = ""
    # if response:
    #     access_token = response.json()['access_token']

    translate.set_host('api.fanyi.baidu.com')
    translate.set_url('/api/trans/vip/translate')
    translate.connect()
    translate.add_param('appid', appid)
    translate.add_param('secretKey', secretKey)
    translate.add_param('from', lan[fromString.get()][1])
    translate.add_param('to', lan[toString.get()][1])

    # ocr.set_url('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token)
    # ocr.set_param('language_type', lan[fromString.get()][0])
    # ocr.set_head('content-type', 'application/x-www-form-urlencoded')


def on_press(event):
    global on_drop
    global pressMousePosition
    global rect
    on_drop = True
    pressMousePosition = screen.get_mouse_position()
    screen.add_mouse_point()
    print('Press')
    if rect is None:
        rect = rect_canvas.create_rectangle(pressMousePosition.x, pressMousePosition.y,
                                            pressMousePosition.x, pressMousePosition.y,
                                            tags='rect', outline='red', width=3)


def on_drop_event(event):
    rect_canvas.coords(rect, (pressMousePosition.x, pressMousePosition.y,
                              event.x, event.y))


@log('set rect')
def on_release(event):
    global on_drop
    # global img_label
    global pressMousePosition
    if pressMousePosition is None:
        return
    on_drop = False
    print('Release')
    screen.add_mouse_point()
    # rect_win.withdraw()
    background_win.withdraw()
    mainWin.deiconify()
    # img_label.destroy()
    img_label = None
    screen.clear()
    screen.set_rect(pressMousePosition.x, pressMousePosition.y,
                    event.x_root, event.y_root)
    pressMousePosition = None


def on_exit(event):
    # global img_label
    global pressMousePosition
    print('Exit set')
    # rect_win.withdraw()
    background_win.withdraw()
    mainWin.deiconify()
    # img_label.destroy()
    # img_label = None
    pressMousePosition = None


on_drop = False
background_win = tk.Toplevel()
background_win.attributes("-fullscreen", True)
background_win.attributes("-alpha", 0.5)
background_win.withdraw()
background_win.attributes('-topmost', 1)
background_win.bind('<ButtonPress-1>', func=on_press)
background_win.bind('<ButtonPress-3>', func=on_exit)
background_win.bind('<ButtonRelease-1>', func=on_release)
background_win.bind('<B1-Motion>', func=on_drop_event)
rect_canvas = tk.Canvas(background_win, bg='grey')
rect_canvas.pack()
pressMousePosition = None
rect = None


def set_rect():
    global background_win
    mainWin.withdraw()
    img = screen.grab()
    background_win.deiconify()
    img = ImageTk.PhotoImage(img)
    rect_canvas.pack_forget()
    rect_canvas.config(width=img.width(), height=img.height())
    rect_canvas.pack()


def show_log():
    log_win = tk.Toplevel()
    log_win.grab_set()
    log_label = tk.Label(log_win, text=log_variable.get())
    log_label.place(relx=0.5, rely=0.5, anchor='center')
    log_win.mainloop()


def set_alpha(x):
    global mainWin_alpha
    mainWin_alpha = setting_scale.get() / 100
    mainWin.wm_attributes("-alpha", mainWin_alpha)


def set_cb():
    mainWin.wm_attributes('-topmost', mainWin_top.get())


mainWin_alpha = 0.8
mainWin_top = None
setting_scale = None


def setting():
    global mainWin_top
    global setting_scale
    setting_win = tk.Toplevel()
    setting_win.geometry('300x150+100+100')
    setting_scale = tk.Scale(setting_win, from_=0, to=100, orient='horizontal', command=set_alpha)
    setting_scale.place(relx=0.5, rely=0.5, anchor='center', y=-15, x=20, width=200, height=45)
    setting_label = tk.Label(setting_win, text='不透明度')
    setting_label.place(relx=0.5, rely=0.5, anchor='center', y=-5, x=-120, height=45)
    mainWin_top = tk.IntVar()
    setting_cb = tk.Checkbutton(setting_win, text='锁定前置窗口', variable=mainWin_top, command=set_cb)
    setting_cb.select()
    setting_cb.place(relx=0.5, rely=0.5, anchor='center', y=20, width=100)
    setting_scale.set(mainWin_alpha * 100)


menubar.add_command(label='Set Rect', command=set_rect)
menubar.add_command(label='Show Rect', command=show)
menubar.add_command(label='Translate', command=trans)
menubar.add_command(label='Setting', command=setting)
menubar.add_command(label='Log', command=show_log)
api_init()

mainWin.mainloop()
quit_app()
