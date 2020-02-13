# Copyright (c) 2018 Viktor Vorobjov
class RelayControl:
    
    '''
    Relay Control
    '''
    
    def __init__(self, name=None, _pin=None, on_value=1, state_on="ON", state_off="OFF", default=0):
        self.name = name
        self._relay = _pin
        self.on_value = on_value
        self.cb = None
        self.state = None
        self.state_on = state_on
        self.state_off = state_off
        self.change_state(default)
        self.mode = None

    def on(self):
        self.change_state(self.on_value)

    def off(self):
        self.change_state(1 - self.on_value)

    def get_state(self):
        self.state = self.state_off

        if self.on_value == self._relay.value():
            self.state = self.state_on

        return self.state

    def change_state(self, reguest_value=None):
        if reguest_value is not None:
            self._relay.value(reguest_value)
        else:
            if self._relay.value() == 1:
                self._relay.value(0)
            else:
                self._relay.value(1)

        self.get_state()

        if self.cb:
            self.cb(self)


    def set_callback(self, f):
        self.cb = f
    