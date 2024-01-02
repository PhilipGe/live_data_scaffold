from enum import Enum
from kivy.uix.boxlayout import BoxLayout
from paramboard.parameter_model import ParameterModel, ParamState
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

class ParameterComponent(BoxLayout):

    def __init__(self, model: ParameterModel, **kwargs):
        super(ParameterComponent, self).__init__(**kwargs)

        self.model: ParameterModel = model

        self.model.register_state_transition_callback(self.on_state_transition)

        self.main_container = BoxLayout(orientation='vertical', padding=(0,0,0,0))

        self.text_input = TextInput(
            disabled = not self.model.enable_input,
            multiline = False
        )
        self.label = Label(text=self.model.label, padding=(0,0,0,self.height/4))
        self.main_container.add_widget(self.text_input)
        self.main_container.add_widget(self.label)

        self.add_widget(self.main_container)

        self.text_input.bind(text=self.on_text_change)

    def on_state_transition(self, state_transition: ParamState):
        if(state_transition == ParamState.Default):
            self.text_input.background_color = (1,1,1,1)
        elif(state_transition == ParamState.ProposedChange):
            self.text_input.background_color = (1,1,0,1)
        elif(state_transition == ParamState.SuccessfulChange):
            self.text_input.background_color = (0,1,0,1)
        elif(state_transition == ParamState.InvalidValue):
            self.text_input.background_color = (1,0,0,1)

    def on_text_change(self, text_instance, new_text):
        self.model.set_proposed_val(new_text)