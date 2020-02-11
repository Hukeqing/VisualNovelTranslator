import pyautogui as pag
import PIL.ImageDraw as imgDraw


class ScreenCut:
    @staticmethod
    def grab(image_filename=None, rect=None):
        return pag.screenshot(imageFilename=image_filename, region=rect)

    def __init__(self):
        self.point = [set(), set()]
        self.rect = None

    def add_point(self, value):
        self.point[0].add(value[0])
        self.point[1].add(value[1])
        if len(self.point[0]) >= 2 and len(self.point[1]) >= 2:
            self.rect = (min(self.point[0]), min(self.point[1]), max(self.point[0]), max(self.point[1]))
            self.rect = (self.rect[0], self.rect[1], self.rect[2] - self.rect[0], self.rect[3] - self.rect[1])
            # self.show_region()

    def clear(self):
        self.point[0].clear()
        self.point[1].clear()

    def cut(self, file=None):
        return self.grab(file, self.rect)

    def add_mouse_point(self):
        self.add_point(pag.position())

    def show_region(self, outline_color='red'):
        screens_im = self.grab()
        draw = imgDraw.Draw(screens_im)
        region = (self.rect[0], self.rect[1], self.rect[2] + self.rect[0], self.rect[3] + self.rect[1])
        draw.rectangle(region, outline=outline_color)
        screens_im.show()


def test_hot_key():
    screen_cut = ScreenCut()
    import time

    time.sleep(2)
    print("add A")
    screen_cut.add_mouse_point()
    time.sleep(2)
    print("add B")
    screen_cut.add_mouse_point()
    img = screen_cut.cut()
    img.show()


if __name__ == '__main__':
    test_hot_key()
