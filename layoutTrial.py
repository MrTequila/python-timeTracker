from kivy.app import App

from kivy.graphics import Ellipse, Color, Rectangle
from kivy.vector import Vector

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button


class CustomLayout(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(CustomLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 1, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=(50, 50), pos=self.pos)
            self.label = Label(text="test")

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 3
        self.position = (100, 100)
        self.size = (250, 250)
        # color = [random(), random(), random(), 1]
        rect1 = Rect()
        self.add_widget(rect1)
        button = Button()
        self.add_widget(button)
        rect2 = Rect()
        # self.add_widget(rect2)
        test1 = TestGrid()
        self.add_widget(test1)
        test2 = TestGrid()
        self.add_widget(test2)
        test3 = TestGrid()
        self.add_widget(test3)


class Rect(CustomLayout):
    def __init__(self, **kwargs):
        super(Rect, self).__init__(**kwargs)


class TestGrid(FloatLayout):
    def __init__(self, **kwargs):
        super(TestGrid, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 1)
            self.rect = Rectangle(size=(50, 50), pos=(100, 100))
            self.label = Label(text="test", pos=(200, 40))
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = (instance.pos[0] + 100, instance.pos[1] + 100)
        print(instance.pos)
        self.label.pos = (instance.pos[0] + 120, instance.pos[1] + 100)


class LayoutTrialApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    LayoutTrialApp().run()
