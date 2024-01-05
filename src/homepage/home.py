from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.event import EventDispatcher

from graphboard.graphboard import GraphBoard
from paramboard.parameter.parameter_component import ParameterComponent
from paramboard.parameter.parameter_model import ParameterModel
from paramboard.button.button_model import ButtonModel
from paramboard.paramboard import ParamBoard
from graphboard.graph.graph_model import GraphModel

class HomePage(BoxLayout, EventDispatcher):
    
    def __init__(self, parameter_models: list[ParameterModel], button_models: list[ButtonModel], graph_models: list[GraphModel], **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.orientation = 'horizontal'

        self.parameter_models = parameter_models
        self.button_models = button_models

        self.add_widget(GraphBoard(graph_models))
        self.add_widget(ParamBoard(parameter_models, button_models))