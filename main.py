import json
import time
import tkinter as tk
import tkinter.ttk
import tkinter.scrolledtext
import tkinter.messagebox

from PIL import ImageTk

from Modular import OCR, Translate
from SystemAPI import *

screen = ScreenCut()

lan = {'中文': 'zh', '日语': 'jp', '英语': 'en', '韩语': 'kor'}
replace_word = dict()

mainWin = tk.Tk()
mainWin.title('Visual Novel Translator')
# mainWin.configure(background='red')
mainWin.wm_attributes('-topmost', 1)
mainWin.wm_attributes("-alpha", 0.8)
mainWin.geometry('1000x150+300+300')

ans_label = tk.Label(mainWin, background="#cccccc", font=('Microsoft YaHei', 10), anchor='center', justify='center')
ans_label.place(relx=0.5, rely=0.5, anchor='center')
# ans_label.config(state='disabled')

menubar = tk.Menu(mainWin)
mainWin.config(menu=menubar)
mainWin.bind('<Configure>', lambda event: ans_label.config(wraplength=mainWin.winfo_width() - 20))

log_variable = tk.StringVar()

fromString = tk.StringVar()
fromString.set('日语')
toString = tk.StringVar()
toString.set('中文')

transHistory = str()

baiduOCR: OCR.BaiduOCR
transAPI = list()


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
    # print(x)
    cur = lan[fromString.get()]
    # ocr.set_param('language_type', cur[0])
    # translate.add_param('from', cur[1])
    baiduOCR.change_lan(cur)
    transAPI[0].set_from_lan(cur)


@log('To Changed')
def change_to(x):
    # print(x)
    cur = lan[toString.get()]
    # translate.add_param('to', cur[1])
    transAPI[0].set_to_lan(cur)


def quit_app():
    mainWin.quit()
    # translate.close()
    transAPI[0].close()
    exit(0)


@log('Clear')
def clear():
    # print("clear")
    screen.clear()


@log('Show')
def show():
    # print("show")
    screen.show_region()


@log('Translate')
def trans():
    ans_label.config(text='Translating')
    img = screen.cut()

    words = baiduOCR.get_ans(img)
    if words == "":
        ans_label.config(text='Distinguish No Words!')
        return
    ans = '原文: ' + words + '\n'
    for key, value in replace_word.items():
        words = words.replace(key, value)
    for tra in transAPI:
        ans += '\n' + tra.get_ans(words)
    ans_label.config(text=ans)
    global transHistory
    transHistory = ans + '-' * 20 + '\n' + transHistory


def api_init():
    f = open('setting.json')
    json_data = json.load(f)
    f.close()
    # OCR
    global baiduOCR
    baiduOCR = OCR.BaiduOCR(json_data['OCR']['apiKey'], json_data['OCR']['SecretKey'])
    # Trans
    # global trans
    trans_data: dict = json_data['translate']
    for key, item in trans_data.items():
        tr = Translate.trans_api_dict[key]
        transAPI.append(tr(item['appid'], item['secretKey']))


def on_press(event):
    # print(event)
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
    background_win.withdraw()
    mainWin.deiconify()
    screen.clear()
    screen.set_rect(pressMousePosition.x, pressMousePosition.y,
                    event.x_root, event.y_root)
    pressMousePosition = None


def on_exit(event):
    # print(event)
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


def set_alpha(x):
    print(x)
    global mainWin_alpha
    mainWin_alpha = setting_scale.get() / 100
    mainWin.wm_attributes("-alpha", mainWin_alpha)


def set_cb():
    mainWin.wm_attributes('-topmost', mainWin_top.get())


mainWin_alpha = 0.8
mainWin_top = tk.IntVar()
mainWin_top.set(1)
setting_scale = None


def setting():
    global mainWin_top
    global setting_scale
    setting_win = tk.Toplevel()
    setting_win.geometry('300x150+100+100')
    setting_win.resizable(0, 0)
    # setting_win.bind('<Configure>', func=lambda x: print(x))
    setting_scale = tk.Scale(setting_win, from_=0, to=100, orient='horizontal', command=set_alpha)
    setting_scale.place(relx=0.5, rely=0.5, anchor='center', y=30, x=20, width=200, height=45)
    setting_label = tk.Label(setting_win, text='不透明度')
    setting_label.place(relx=0.5, rely=0.5, anchor='center', y=30, x=-120, height=45)

    # mainWin_top = tk.IntVar()
    setting_cb = tk.Checkbutton(setting_win, text='锁定前置窗口', variable=mainWin_top, command=set_cb)
    if mainWin_top.get():
        setting_cb.select()
    setting_cb.place(relx=0.5, rely=0.5, anchor='center', y=10, width=100)
    setting_scale.set(mainWin_alpha * 100)

    from_combobox = tk.ttk.Combobox(setting_win, textvariable=fromString, width=10)
    from_combobox['value'] = tuple(lan.keys())
    from_combobox.current(1)
    from_combobox.bind("<<ComboboxSelected>>", change_from)
    from_combobox.place(relx=0.5, rely=0.5, anchor='center', y=-45)

    from_label = tk.Label(setting_win, text='原语言')
    from_label.place(relx=0.5, rely=0.5, anchor='center', y=-45, x=-120)

    to_combobox = tk.ttk.Combobox(setting_win, textvariable=toString, width=10)
    to_combobox['value'] = tuple(lan.keys())
    to_combobox.current(0)
    to_combobox.bind("<<ComboboxSelected>>", change_to)
    to_combobox.place(relx=0.5, rely=0.5, anchor='center', y=-20)

    to_label = tk.Label(setting_win, text='翻译语言')
    to_label.place(relx=0.5, rely=0.5, anchor='center', y=-20, x=-120)


replace_setting_text: tk.scrolledtext.ScrolledText


def save_replace():
    res: str = replace_setting_text.get('1.0', tkinter.END)
    global replace_word
    replace_word = dict()
    try:
        for line in res.split('\n'):
            if line == '':
                continue
            data = line.split(':')
            replace_word[data[0]] = data[1]
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('Error', 'Text format error')


def replace_setting():
    global replace_setting_text
    replace_setting_win = tk.Toplevel()
    replace_setting_win.geometry('300x400+300+300')
    replace_setting_win.attributes('-topmost', 1)
    replace_setting_text = tk.scrolledtext.ScrolledText(replace_setting_win)
    replace_setting_text.place(relx=0.5, rely=0.5, y=-20, anchor='center', width=250, height=350)
    for key, value in replace_word.items():
        replace_setting_text.insert(tkinter.END, key + ' : ' + value + '\n')
    replace_setting_button = tk.Button(replace_setting_win, text='Save', command=save_replace)
    replace_setting_button.place(relx=0.5, rely=1, y=-20, anchor='center')
    replace_setting_win.mainloop()


def history():
    history_win = tk.Toplevel()
    history_win.geometry('1000x400+300+300')
    history_win.attributes('-topmost', 1)
    history_win.grab_set()
    history_label = tk.scrolledtext.ScrolledText(history_win)
    history_label.insert('end', transHistory)
    history_label.place(relx=0.5, rely=0.5, anchor='center', width=800, height=300)
    history_win.mainloop()


def show_log():
    log_win = tk.Toplevel()
    log_win.grab_set()
    log_label = tk.Label(log_win, text=log_variable.get())
    log_label.place(relx=0.5, rely=0.5, anchor='center')
    log_win.mainloop()


menubar.add_command(label='Set Rect', command=set_rect)
menubar.add_command(label='Show Rect', command=show)
menubar.add_command(label='Translate', command=trans)
menubar.add_command(label='Replace', command=replace_setting)
menubar.add_command(label='Setting', command=setting)
menubar.add_command(label='History', command=history)
menubar.add_command(label='Log', command=show_log)
api_init()

mainWin.mainloop()
quit_app()
