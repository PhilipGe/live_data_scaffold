import math
from kivy.garden.graph import Graph
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
import numpy as np

from graphboard.graph.graph_model import GraphModel

class GraphTile(BoxLayout):
    
    def __init__(self, graph_model: GraphModel, **kwargs):
        super(GraphTile, self).__init__(**kwargs)
        self.graph_model: GraphModel = graph_model
        self.orientation = 'horizontal'
        self.padding = (10,10,10,10)

        self.graph = Graph(
            xlabel = graph_model.x_label,
            ylabel = graph_model.y_label,
            xmin = graph_model.x_bounds[0],
            xmax = graph_model.x_bounds[1],
            ymin = graph_model.y_bounds[0],
            ymax = graph_model.y_bounds[1],
            x_grid=True,
            x_ticks_major = (graph_model.x_bounds[1]-graph_model.x_bounds[0])/10,
            x_grid_label=True,
            y_grid=True,
            y_ticks_major = (graph_model.y_bounds[1]-graph_model.y_bounds[0])/10,
            y_grid_label=True,
            padding = 2
        )

        self.add_widget(self.graph)

        self.custombox = GridLayout(cols=1, size_hint_x=None, width=150,spacing=15)

        self.add_widget(self.custombox)

        self.add_text_box('xmin', lambda v: self.set_xmin(v.text))
        self.add_text_box('xmax', lambda v: self.set_xmax(v.text))
        self.add_text_box('ymin', lambda v: self.set_ymin(v.text))
        self.add_text_box('ymax', lambda v: self.set_ymax(v.text))

        self.add_button('Autoscale (x)', lambda b: self.autoscale_x())
        self.add_button('Autoscale (y)', lambda b: self.autoscale_y())

        self.custombox.add_widget(Widget())
    
    def add_text_box(self, label, action):
        input = TextInput(size_hint_y=None, height=30, multiline=False)
        input.bind(on_text_validate=action)
        label = Label(text=label, size_hint_y=None, height=20)

        self.custombox.add_widget(input)
        self.custombox.add_widget(label)

    def add_button(self, label, action):
        button = Button(text=label)
        button.bind(on_press=action)
        
        self.custombox.add_widget(button)

    def set_xmin(self, val):
        self.graph.xmin = val
        self.update_ticks()

    def set_xmax(self, val):
        self.graph.xmax = val
        self.update_ticks()
    
    def set_ymin(self, val):
        self.graph.ymin = val
        self.update_ticks()

    def set_ymax(self, val):
        self.graph.ymax = val
        self.update_ticks()

    def update_ticks(self):
        available_sizes = [0.1,1,5,10,15,20]

        xs = 20
        for s in available_sizes:
            if((self.graph.xmax - self.graph.xmin)/s < 10):
                xs = s
                break
        self.graph.x_ticks_major = xs
        
        ys = 20
        for s in available_sizes:
            if((self.graph.ymax - self.graph.ymin)/s < 10):
                ys = s
                break
        self.graph.y_ticks_major = ys

    def autoscale_x(self):
        xmin = np.inf
        xmax = -np.inf

        for s in self.graph_model.streams:
            if(s.minx < xmin): xmin = s.minx
            if(s.maxx > xmax): xmax = s.maxx
        
        self.graph.xmin = xmin
        self.graph.xmax = xmax
        self.update_ticks()
        

    def autoscale_y(self):
        ymin = np.inf
        ymax = -np.inf

        for s in self.graph_model.streams:
            if(s.miny < ymin): ymin = s.miny
            if(s.maxy > ymax): ymax = s.maxy

        self.graph.ymin = ymin
        self.graph.ymax = ymax
        self.update_ticks()