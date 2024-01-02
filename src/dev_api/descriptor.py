from time import sleep
from typing import Callable, Tuple
from kivy.app import App
from kivy.clock import Clock
from threading import Thread, Event

from homepage.home import HomePage

import numpy as np
from paramboard.parameter_model import ParameterModel, ParamState
from paramboard.button_model import ButtonModel
from graphboard.graph_model import GraphModel
from graphboard.plot_model import PlotModel
from graphboard.graph_colors import GraphColors

class SensorPlotter(App):

    def __init__(self, home: HomePage, **kwargs):
        super(SensorPlotter, self).__init__(**kwargs)
        self.home = home

    def build(self):
        return self.home
    
class AppBuilder:

    def __init__(self):
        self.parameter_models: list[ParameterModel] = []
        self.button_models: list[ButtonModel] = []
        self.graph_models: list[GraphModel] = []

        self.indicator_streams: list[Callable[[],None]] = []
        self.point_stream: list[Callable[[],None]] = []
        # self.plot_streams: Callable[[*PlotModel], None] = []

        self.num_graphs: int = 0
        self.streams: list[Callable[[], np.array]] = []

    def add_parameter(self, label:str, input_enabled: bool = True, validator: Callable[[str],bool] = lambda x: True):
        if(0 != len(list(filter(lambda x: x.label == label, self.parameter_models)))): ValueError('Each parameter must have a unique label')

        self.parameter_models.append(ParameterModel(label, input_enabled, validator))

    # The 'parameters involved' should be a list of label parameters, in the order in which their text field values
    # Will be passed into the callback function
    def add_button(self, button_label, parameters_invovled: list[str], callback: Callable[[str],None]):
        if(0 != len(list(filter(lambda x: x.button_label == button_label, self.button_models)))): ValueError('Each button must have a unique label')

        param_models = []
        for label in parameters_invovled:
            p = list(filter(lambda m: m.label == label, self.parameter_models))
            if(len(p) != 1): raise ValueError(f'The number of labels {label} is {len(p)}. Should be exactly 1.')
            param_models.append(p[0])

        self.button_models.append(ButtonModel(button_label, param_models,callback))

    # The 'parameters involved' should be a list of label parameters, in the order in which their update callbacks
    # Will be passed into the callback function. Example of stream callback below that updates paramters with labels 
    # p1 and p2 every 1 second with a different value each
    # 
    # PARAMETERS INVOLVED: ['p1', 'p2']
    # CALLBACK:     def stream_1(p1_update, p2_update): 
    #                   p1_update(str(counter))
    #                   p2_update(str(counter2))
    #                   counter1 += 1
    #                   counter2 -= 1
    
    def add_indicator_stream(self,  parameters_invovled: list[str], callback: Callable[[Tuple[Callable[[str],None],...]], None]):
        param_model_event_dispatches = []

        for label in parameters_invovled:
            p = list(filter(lambda m: m.label == label, self.parameter_models))
            if(len(p) != 1): raise ValueError(f'The number of labels {label} is {len(p)}. Should be exactly 1.')
            param_model_event_dispatches.append(
                lambda new_val, p=p[0]: p.set_active_val_from_stream_update(new_val)
            )

        self.indicator_streams.append(lambda: callback(*param_model_event_dispatches))

    def add_graph(self, title, x_label, y_label):
        if(0 != len(list(filter(lambda x: x.title == title, self.graph_models)))): ValueError('Each graph must have a unique title')

        self.graph_models.append(
            GraphModel(title=title, x_label=x_label, y_label=y_label)
        )

    def add_point_stream(self, graph_title, point_stream: Callable[[],list[Tuple[int,int]]], poll_interval_s=1, cumulative=True, max_num_points = 100):
        g_list: list[GraphModel] = list(filter(lambda x: x.title == graph_title, self.graph_models))
        if(len(g_list) != 1): raise ValueError('Either more than one, or no graphs, exist with this title')

        g = g_list[0]

        g.add_plot(
            PlotModel(point_stream, poll_interval_s, cumulative, max_num_points, color=GraphColors.get_next_plot_color())
        )

    def build_app(self) -> App:

        for f in self.indicator_streams: Clock.schedule_interval(lambda dt, f=f: f(), 1)
        for g in self.graph_models: g.initiate_plot_streams()
        
        return SensorPlotter(HomePage(self.parameter_models, self.button_models, self.graph_models))