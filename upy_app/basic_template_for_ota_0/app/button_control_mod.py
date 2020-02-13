from button_control import ButtonControl
from machine import Pin


class ButtonControlActivate:

    def __init__(self, mbus=False):
        self.mbus = mbus

        self._make_button("btn_left", {"pin": 4})
        self._make_button("btn_right", {"pin": 5})


    def _make_button(self, key, value ):

        ctrl_name = "{}".format(key)
        ctrl_pin = value["pin"]
        ctrl_pin = Pin(ctrl_pin, Pin.IN, Pin.PULL_UP)

        btn_ctrl = ButtonControl(name=ctrl_name, _pin=ctrl_pin, on_value=1)
        btn_ctrl.set_callback(self.ctl_cb)


    def ctl_cb(self, ctrl):

        if self.mbus:
            self.mbus.pub({
                            "id": ctrl.name,
                            "msg": {"name": "state", "data": ctrl.state}
                            })
