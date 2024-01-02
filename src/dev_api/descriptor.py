from typing import Callable
from kivy.app import App
from kivy.clock import Clock

from homepage.home import HomePage

import numpy as np
from paramboard.parameter_model import ParameterModel, ParamState
from paramboard.button_model import ButtonModel

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
        self.callbacks: list[Callable[[list[ParameterModel]],None]] = []

        self.num_graphs: int = 0
        self.streams: list[Callable[[], np.array]] = []

    def add_parameter(self, label:str, input_enabled: bool = True, validator: Callable[[str],bool] = lambda x: True):
        self.parameter_models.append(ParameterModel(label, input_enabled, validator))

    # The 'parameters involved' should be a list of label parameters, in the order in which their text field values.
    # Will be passed into the callback function
    def add_button(self, button_label, parameters_invovled: list[str], callback: Callable[[str],None]):
        param_models = []
        for label in parameters_invovled:
            p = list(filter(lambda m: m.label == label, self.parameter_models))
            if(len(p) != 1): raise ValueError(f'The number of labels {label} is {len(p)}. Should be exactly 1.')
            param_models.append(p[0])

        self.button_models.append(ButtonModel(button_label, param_models,callback))
        
    def set_num_graphs(self, num_graphs):
        self.graph_num = num_graphs

    def add_stream(self, graph_id, stream: Callable[[], np.array]):
        pass

    def build_app(self) -> App:
        return SensorPlotter(HomePage(self.parameter_models, self.button_models))