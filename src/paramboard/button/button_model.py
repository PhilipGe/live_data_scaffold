from enum import Enum
from functools import reduce
from typing import Callable
from paramboard.parameter.parameter_model import ParameterModel
from kivy.clock import Clock

class ButtonState(Enum):
    Default = 'Default'
    SuccessfulChange = 'SuccessfulChange'
    Error = 'Error'

class ButtonModel:
    
    def __init__(self, action_label, parameters_invovled: list[ParameterModel], callback: Callable[[str], None], **kwargs):
        self.action_label = action_label
        self.parameters_involved: list[ParameterModel] = parameters_invovled
        self.callback = callback

        self.state = ButtonState.Default

        self.state_transition_callback = None

    def register_state_transition_callback(self, callback):
        self.state_transition_callback = callback
    
    def parameters_being_observed_changed(self):
        return reduce(lambda acc, p_model: acc or p_model.param_changed(), self.parameters_involved, False)
    
    def parameters_being_observed_have_valid_inputs(self):
        return reduce(lambda acc, p_model: acc and p_model.validate_input(), self.parameters_involved, True)
    
    def button_clicked(self, button_component_instance):
        if(self.parameters_being_observed_changed()):
            if(self.parameters_being_observed_have_valid_inputs()):
                self.callback(*map(lambda p_model: p_model.proposed_val, self.parameters_involved))
                for p in self.parameters_involved: p.change_proposed_val_to_active_val()
                self.transition_states(ButtonState.SuccessfulChange)
            else: 
                self.transition_states(ButtonState.Error)
        
    def transition_states(self, new_state: ButtonState):
        if(self.state_transition_callback == None): raise ValueError('The state transition callback was never set')
        self.state = new_state
        self.state_transition_callback(new_state)
        if(new_state == ButtonState.SuccessfulChange or new_state == ButtonState.Error):
            Clock.schedule_once(lambda dt: self.transition_states(ButtonState.Default), 0.4)