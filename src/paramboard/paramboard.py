from threading import Thread
from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from paramboard.parameter_model import ParameterModel
from paramboard.button_model import ButtonModel
from paramboard.button_component import ButtonComponent
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from paramboard.parameter_component import ParameterComponent

class ParamBoard(BoxLayout):

    def __init__(self, param_models: list[ParameterModel], button_models: list[ButtonModel], num_cols = 3,  **kwargs):
        super(ParamBoard, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.background_color = (1,0,0,1)

        self.parameter_components: list[ParameterComponent] = []
        self.button_components: list[ButtonComponent] = []
        
        self.padding = 50

        self.grid_layout = GridLayout(cols=num_cols, row_force_default=True, row_default_height=120, spacing=10)

        self.add_parameters(param_models)

        self.add_widget(self.grid_layout)

        self.button_box_layout = GridLayout(cols = num_cols, size_hint_y=0.2, spacing=10)

        self.add_buttons(button_models)

        self.add_widget(self.button_box_layout)

        self.reset_fields_button = Button(text='Reset Fields')
        self.reset_fields_button.bind(on_press=self.reset_fields)
        self.button_box_layout.add_widget(self.reset_fields_button)

    def reset_fields(self, button_instance):
        for p_c in self.parameter_components:
            p_c.reset_field()

    def add_parameters(self, param_models: list[ParameterModel]):
        self.parameter_components += [ParameterComponent(m) for m in param_models]

        for p in self.parameter_components:
            self.grid_layout.add_widget(p)

    def add_buttons(self, button_models: list[ButtonModel]):
        self.button_components = [ButtonComponent(m) for m in button_models]

        for b in self.button_components:
            self.button_box_layout.add_widget(b)