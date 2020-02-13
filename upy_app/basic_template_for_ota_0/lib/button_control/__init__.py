# Copyright (c) 2018 Viktor Vorobjov
#  Holtek - Touch I/O Flash MCU BS83A02A-4/BS83A04A-3/BS83A04A-4
#  Touch pin button - TTP223
#  Mechanical Pin button

import uasyncio as asyncio

class ButtonControl:

    def __init__(self, name=None, _pin=False, on_value=1,
                 state_on="ON", state_off="OFF"):

        self._switch = _pin
        self.name = name

        self.button = None

        self.on_value = on_value
        self.off_value = 1-on_value

        self.state_on = state_on
        self.state_off = state_off

        self._value = 1-on_value

        self.cb = None
        self.state = None

        self.change_state()

        self.debounce_ms = 300

        loop = asyncio.get_event_loop()
        loop.create_task(self.push_check())



    def change_state(self):
        self._value = self._switch.value()

        if self._value == self.on_value:
            self.state = self.state_on
        elif self._value == self.off_value:
            self.state = self.state_off

        if self.cb:
            self.cb(self)

    async def push_check(self):
        while True:
            if self._switch and self._switch.value() != self._value:
                self.change_state()
            await asyncio.sleep_ms(self.debounce_ms)


    def set_callback(self, f):
        self.cb = f






