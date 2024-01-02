from enum import Enum
from kivy.uix.boxlayout import BoxLayout
from paramboard.button_model import ButtonModel, ButtonState
from kivy.uix.button import Button

class ButtonComponent(Button):

    def __init__(self, model: ButtonModel, **kwargs):
        super(ButtonComponent, self).__init__(**kwargs)

        self.model: ButtonModel = model
        self.text = model.action_label
        self.model.register_state_transition_callback(self.on_state_transition)

        self.bind(on_press=self.model.button_clicked)

    def on_state_transition(self, state_transition: ButtonState):
        if(state_transition == ButtonState.Default):
            self.background_color = (1,1,1,1)
        elif(state_transition == ButtonState.SuccessfulChange):
            self.background_color = (0,1,0,1)
        elif(state_transition == ButtonState.Error):
            self.background_color = (1,0,0,1)