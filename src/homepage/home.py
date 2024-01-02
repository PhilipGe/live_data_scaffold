from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder

from graphboard.graphboard import GraphBoard
from paramboard.parameter_component import ParameterComponent
from paramboard.parameter_model import ParameterModel
from paramboard.button_model import ButtonModel
from paramboard.paramboard import ParamBoard

class HomePage(BoxLayout):
    
    def __init__(self, parameter_models: list[ParameterModel], button_models: list[ButtonModel], **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.orientation = 'horizontal'

        self.parameter_models = parameter_models
        self.button_models = button_models

        self.add_widget(GraphBoard())
        self.add_widget(ParamBoard(parameter_models, button_models))