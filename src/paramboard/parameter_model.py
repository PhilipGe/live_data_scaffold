from enum import Enum
from typing import Callable
from kivy.clock import Clock

class ParamState(Enum):
    Default = 'Default'
    ProposedChange = 'ProposedChange'
    SuccessfulChange = 'SuccessfulChange'
    InvalidValue = 'InvalidValue'

class ParameterModel:

    def __init__(self, label: str, enable_input: bool, validator: Callable[[str],bool]):
        self.label = label
        self.validator = validator
        self.enable_input = enable_input

        self.state = ParamState.Default

        self.state_transition_callback = None
        self.stream_update_callback = None

        # For display parameter
        self.active_val = ""

        # For input parameter
        self.proposed_val = self.active_val

    def param_changed(self) -> bool:
        return self.active_val != self.proposed_val
    
    def set_proposed_val(self, new_val):
        self.proposed_val = new_val
        if(self.param_changed()):
            if(self.validate_input()):
                self.transition_states(ParamState.ProposedChange)
            else:
                self.transition_states(ParamState.InvalidValue)
        else:
            self.transition_states(ParamState.Default)

    def validate_input(self) -> bool:
        return self.validator(self.proposed_val)
    
    def change_proposed_val_to_active_val(self):
        if(not self.validate_input()): raise ValueError('This function should never be called if the input is not validated prior')
        self.active_val = self.proposed_val
        self.transition_states(ParamState.SuccessfulChange)

    def set_active_val_from_stream_update(self, new_active_val):
        self.active_val = new_active_val
        self.proposed_val = new_active_val
        if(not self.validate_input()): 
            self.transition_states(ParamState.InvalidValue)
            print(f"WARNING: data coming from stream into parameter with label {self.label} does not pass parameter's validator function. Data in question: {new_active_val}")
        # else: self.transition_states(ParamState.SuccessfulChange)

        if(self.stream_update_callback != None): self.stream_update_callback()
        

    def register_state_transition_callback(self, state_transition_callback: Callable[[ParamState],None]):
        self.state_transition_callback = state_transition_callback

    def register_stream_update_callback(self, stream_update_callback):
        self.stream_update_callback = stream_update_callback

    def transition_states(self, new_state: ParamState):
        if(self.state_transition_callback == None): raise ValueError('The state transition callback was never set')
        self.state = new_state
        self.state_transition_callback(new_state)
        if(new_state == ParamState.SuccessfulChange):
            Clock.schedule_once(lambda dt: self.transition_states(ParamState.Default), 0.4)