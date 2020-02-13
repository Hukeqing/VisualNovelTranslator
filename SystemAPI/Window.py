import tkinter as tk


class Event:
    def __init__(self, event, va, sva):
        self.x = event.x
        self.y = event.y
        self.globe_x = event.x_root
        self.globe_y = event.y_root
        self.value = va
        self.symValue = sva


class Widget:
    def __init__(self, type_name, parent=None):
        self.root = type_name()
        self.parent = parent
        # EVENT
        self.buttonPressEvent = None
        self.buttonReleaseEvent = None
        self.mouseWheel = None
        self.keyEvent = None

        self.root.bind(sequence="<ButtonPress>", func=self.button_press_event)
        self.root.bind(sequence="<ButtonRelease>", func=self.button_release_event)
        self.root.bind(sequence='<MouseWheel>', func=self.mouse_wheel)
        self.root.bind(sequence='<Key>', func=self.key_event)

    def button_press_event(self, event):
        if self.buttonPressEvent is not None:
            self.buttonPressEvent(Event(event, event.num, event.num))

    def button_release_event(self, event):
        if self.buttonReleaseEvent is not None:
            self.buttonReleaseEvent(Event(event, event.num, event.num))

    def key_event(self, event):
        if self.buttonReleaseEvent is not None:
            self.buttonReleaseEvent(Event(event, event.char, event.keysym))

    def mouse_wheel(self, event):
        if self.buttonReleaseEvent is not None:
            self.buttonReleaseEvent(Event(event, event.delta, event.delta))

    def place(self, basic='center', x=0, y=0, width=None, height=None):
        if isinstance(self.root, tk.Tk) or isinstance(self.root, tk.Toplevel):
            self.root.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
        else:
            self.root.place(relx=0.5, rely=0.5, anchor=basic, x=x, y=y, width=width, height=height)


class Window(Widget):
    def __init__(self, sub_window=False):
        super().__init__(tk.Tk if not sub_window else tk.Toplevel)

    def set_title(self, title):
        self.root.title(title)

    def set_geometry(self, width, height, x, y):
        self.root.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))

    def add_attributes(self, key, value):
        self.root.wm_attributes(key, value)

    def set_fullscreen(self):
        self.add_attributes("-fullscreen", True)

    def exit_fullscreen(self):
        self.add_attributes("-fullscreen", False)

    def start(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()


class Label(Widget):
    def __init__(self, parent=None, text=""):
        super().__init__(tk.Label, parent)
        self.root: tk.Label


if __name__ == '__main__':
    test = Window()
    test.root.mainloop()
