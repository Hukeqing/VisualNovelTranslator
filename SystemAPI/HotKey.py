import ctypes
import ctypes.wintypes
from threading import Thread, activeCount, enumerate


class KeyCode:
    MOD_ALT = 1
    MOD_CONTROL = 2
    MOD_SHIFT = 4
    MOD_WIN = 8

    LBUTTON = 1
    RBUTTON = 2
    CANCEL = 3
    MBUTTON = 4
    BACK = 8
    TAB = 9
    CLEAR = 12
    RETURN = 13
    SHIFT = 16
    CONTROL = 17
    MENU = 18
    PAUSE = 19
    CAPITAL = 20
    KANA = 21
    HANGEUL = 21  # old name - should be here for compatibility
    HANGUL = 21
    JUNJA = 23
    FINAL = 24
    HANJA = 25
    KANJI = 25
    ESCAPE = 27
    CONVERT = 28
    NONCONVERT = 29
    ACCEPT = 30
    MODECHANGE = 31
    SPACE = 32
    PRIOR = 33
    NEXT = 34
    END = 35
    HOME = 36
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40
    SELECT = 41
    PRINT = 42
    EXECUTE = 43
    SNAPSHOT = 44
    INSERT = 45
    DELETE = 46
    HELP = 47
    LWIN = 91
    RWIN = 92
    APPS = 93
    NUMPAD0 = 96
    NUMPAD1 = 97
    NUMPAD2 = 98
    NUMPAD3 = 99
    NUMPAD4 = 100
    NUMPAD5 = 101
    NUMPAD6 = 102
    NUMPAD7 = 103
    NUMPAD8 = 104
    NUMPAD9 = 105
    MULTIPLY = 106
    ADD = 107
    SEPARATOR = 108
    SUBTRACT = 109
    DECIMAL = 110
    DIVIDE = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    NUMLOCK = 144
    SCROLL = 145
    LSHIFT = 160
    RSHIFT = 161
    LCONTROL = 162
    RCONTROL = 163
    LMENU = 164
    RMENU = 165
    PROCESSKEY = 229
    ATTN = 246
    CRSEL = 247
    EXSEL = 248
    EREOF = 249
    PLAY = 250
    ZOOM = 251
    NONAME = 252
    PA1 = 253
    OEM_CLEAR = 254
    # multi-media related "keys"
    MOUSEEVENTF_XDOWN = 0x0080
    MOUSEEVENTF_XUP = 0x0100
    MOUSEEVENTF_WHEEL = 0x0800
    XBUTTON1 = 0x05
    XBUTTON2 = 0x06
    VOLUME_MUTE = 0xAD
    VOLUME_DOWN = 0xAE
    VOLUME_UP = 0xAF
    MEDIA_NEXT_TRACK = 0xB0
    MEDIA_PREV_TRACK = 0xB1
    MEDIA_PLAY_PAUSE = 0xB3
    BROWSER_BACK = 0xA6
    BROWSER_FORWARD = 0xA7


class HotKey:
    user32 = ctypes.windll.user32  # 加载user32.dll

    class HotKeyList:
        def __init__(self):
            self.name = dict()
            self.key = dict()
            self.func = dict()
            self.cnt = 0

        def add_key(self, name, key, func):
            self.name[self.cnt] = name
            self.key[self.cnt] = key
            self.func[self.cnt] = func
            self.cnt += 1
            return self.cnt - 1

    @staticmethod
    def thread_it(func, *args):
        t = Thread(target=func, args=args, daemon=True)
        t.start()
        return t

    def __init__(self):
        super().__init__()
        self.keyList = HotKey.HotKeyList()
        self.end = False

    def add_key(self, name, key, func):
        self.keyList.add_key(name, key, func)

    def register_key(self, hwnd=None, flag_id=0, fn_key=0, v_key=0):  # 注册热键，默认一个alt+F9
        if isinstance(v_key, str):
            v_key = ord(v_key.upper())
        return self.user32.RegisterHotKey(hwnd, flag_id, fn_key, v_key)

    def log(self):
        print('HotKeyCount:', self.keyList.cnt)
        for index, name in self.keyList.name.items():
            print('ID: ', index, 'Name:', name, 'Function:', self.keyList.func[index])
        count = activeCount()
        print("当前总线程数量:", count)
        print('当前线程列表:', enumerate())
        print('热键注册初始化完毕')

    def start(self):
        self.log()
        self.thread_it(self.run)

    def run(self):
        for i in range(self.keyList.cnt):
            if not self.register_key(None, i, *self.keyList.key[i]):
                print('register hot key fail！ id:', i)
        # 以下为检测热键是否被按下，并在最后释放快捷键
        try:
            msg = ctypes.wintypes.MSG()
            while True:
                if not self.end and self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == 786:  # win32con.WM_HOTKEY = 786
                        if msg.wParam in self.keyList.name.keys():
                            self.thread_it(self.keyList.func[msg.wParam])
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        except Exception as e:
            print(e)
            exit(0)

    def stop(self):
        # 必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，
        # 那么下次很可能就没办法注册成功了，这时可以换一个热键测试
        for i in range(self.keyList.cnt):
            self.user32.UnregisterHotKey(None, i)
        self.end = True


def test_hot_key():
    global END
    END = False

    def test_start():
        print("按下了开始键...the program is running")

    def test_stop():
        print("按下了停止键...the program is stopped")

    def test_quit():
        global END
        END = True
        print("END")

    hot_key = HotKey()
    hot_key.add_key('start', (KeyCode.MOD_ALT, KeyCode.F9), test_start)
    hot_key.add_key('stop', (KeyCode.MOD_CONTROL, 's'), test_stop)
    hot_key.add_key('quit', (0, KeyCode.ESCAPE), test_quit)

    hot_key.start()
    while not END:
        pass
    hot_key.stop()


if __name__ == '__main__':
    test_hot_key()
