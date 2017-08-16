from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.graphics import Ellipse, Color, Rectangle
from math import atan2, sqrt, pow, degrees, sin, cos, radians
from kivy.vector import Vector

from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListView, ListItemButton, CompositeListItem, ListItemLabel
from random import random


class MainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        btn = Button(text='Exit',
                     size_hint=(None, None),
                     width=150,
                     height=100)
        self.add_widget(btn)
        in_data = {"Opera": 350,
                   "Steam": 234,
                   "Overwatch": 532,
                   "PyCharm": 485,
                   "YouTube": 221}
        chart = PieChart(data=in_data)
        self.add_widget(chart)

        list_item_args_converter = lambda row_index, rec: {
            'text': list(in_data.keys())[row_index] + " - " \
                    + str(in_data[list(in_data.keys())[row_index]]) + " minutes",
            'size_hint_y': None,
            'height': 25,
            'cls_dicts': [{'cls': ListItemLabel,
                           'kwargs': {'text': list(in_data.keys())[row_index]}},
                          {'cls': ListItemLabel,
                           'kwargs': {'text': str(in_data[list(in_data.keys())[row_index]])}},
                          {'cls': ListItemButton,
                           'kwargs': {'text': "Add to category"}}]
        }

        dict_adapter = DictAdapter(
            sorted_keys=sorted(in_data.keys()),
            data=in_data,
            selection_mode='single',
            args_converter=list_item_args_converter,
            cls=CompositeListItem)

        lista = ListView(adapter=dict_adapter,
                         size_hint=(.2, 1.0))
        self.add_widget(lista)


class ProcessView(ListView):
    def __init__(self, data, **kwargs):
        super(ProcessView, self).__init__(**kwargs)


# TODO Graphic representation of results, ie. PieChart or BarChart
class PieChart(GridLayout):
    def __init__(self, data, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 5
        angle_start = 0
        count = 0
        for key, value in data.items():
            percentage = (value / sum(data.values()) * 100)
            angle_end = angle_start + 3.6 * percentage
            color = [random(), random(), random(), 1]
            # add part of Pie
            temp = PiePart(pos=(200, 230), size=(200, 200),
                           angle_start=angle_start,
                           angle_end=angle_end, color=color, name=key)
            self.add_widget(temp)
            angle_start = angle_end
            # add legend (rectangle and text)
            legend = Legend(pos=(200, 200 - count * 30),
                            size=(200, 200),
                            color=color,
                            name=key,
                            value=percentage)
            self.add_widget(legend)
            self.canvas.ask_update()
            count += 1


class PiePart(Widget):
    def __init__(self, pos, color, size, angle_start, angle_end, name, **kwargs):
        super(PiePart, self).__init__(**kwargs)
        # Window.bind(mouse_pos=self.on_mouse_pos)
        self.moved = False
        self.angle = 0
        self.name = name
        with self.canvas:
            Color(*color)
            self.c = Ellipse(pos=pos, size=size,
                             angle_start=angle_start,
                             angle_end=angle_end)

    def move_pie_out(self):
        ang = self.c.angle_start + (self.c.angle_end - self.c.angle_start) / 2
        vect_x = cos(radians(ang - 90)) * 50
        vect_y = sin(radians(ang + 90)) * 50
        if not self.moved:
            self.c.pos = Vector(vect_x, vect_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = True
        else:
            self.c.pos = Vector(-vect_x, -vect_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = False

    def move_pie_in(self):
        ang = self.c.angle_start + (self.c.angle_end - self.c.angle_start) / 2
        vect_x = cos(radians(ang - 90)) * 50
        vect_y = sin(radians(ang + 90)) * 50
        if self.moved:
            self.c.pos = Vector(-vect_x, -vect_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = False

    def on_touch_down(self, touch):
        if self.is_inside_pie(*touch.pos):
            self.move_pie_out()

    def is_inside_pie(self, *touch_pos):
        y_pos = touch_pos[1] - self.c.pos[1] - self.c.size[1] / 2
        x_pos = touch_pos[0] - self.c.pos[0] - self.c.size[0] / 2
        angle = degrees(1.5707963268 - atan2(y_pos, x_pos))
        if angle < 0:
            angle += 360
        self.angle = angle
        radius = sqrt(pow(x_pos, 2) + pow(y_pos, 2))
        if self.c.angle_start < angle < self.c.angle_end:
            return radius < self.c.size[0] / 2


# TODO add a legend with color rectangle, numeric value and name
class Legend(Widget):
    def __init__(self, pos, size, color, name, value, **kwargs):
        super(Legend, self).__init__(**kwargs)
        self.name = name
        with self.canvas:
            Color(*color)
            Rectangle(pos=(pos[0] + size[0] * 1.3, pos[1] + size[1] * 0.9),
                      size=(size[0] * 0.1, size[1] * 0.1))
            self.label = Label(text=str("%.2f" % value + "% - " + name),
                               pos=(pos[0] + size[0] * 1.7, pos[1] + size[1] * 0.7),
                               halign='left',
                               text_size=(200, 20))

            print(("%.2f" % value + "% - " + name))


class TrackerApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    TrackerApp().run()
