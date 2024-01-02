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
        self.model.register_stream_update_callback(self.stream_update)

        self.main_container = BoxLayout(orientation='vertical', padding=(0,0,0,0))

        self.text_input = TextInput(
            disabled = not self.model.enable_input,
            multiline = False
        )
        self.label = Label(text=self.model.label, padding=(0,0,0,self.height/4))
        self.text_input.bind(text=self.on_text_change)
        self.main_container.add_widget(self.text_input)
        self.main_container.add_widget(self.label)

        self.add_widget(self.main_container)

    def reset_field(self):
        self.text_input.text = self.model.active_val
        self.model.transition_states(ParamState.Default)

    def stream_update(self):
        self.text_input.text = self.model.active_val

    def on_state_transition(self, state_transition: ParamState):
        if(state_transition == ParamState.Default):
            self.text_input.background_color = (1,1,1,1)
        elif(state_transition == ParamState.ProposedChange):
            self.text_input.background_color = (1,1,0,1)
        elif(state_transition == ParamState.SuccessfulChange):
            self.text_input.background_color = (0,1,0,1)
        elif(state_transition == ParamState.InvalidValue):
            self.text_input.background_color = (1,0,0,1)

    def on_stream_update(self, new_val: str):
        self.text_input.text = new_val

    def on_text_change(self, parameter_component, new_text):
        self.model.set_proposed_val(new_text)