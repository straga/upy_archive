from relay_control import RelayControl
from machine import Pin

import uasyncio as asyncio

class RelayControlActivate:

    def __init__(self, mbus):

        self.mbus = mbus
        self.relays = {}

        self._make_realay("pump_1", {"pin": 25})
        self._make_realay("light_1", {"pin": 26})
        self._make_realay("light_2", {"pin": 27})


    def _make_realay(self, key, value):
        relay_pin = value["pin"]
        relay_name = "{}".format(key)
        relay_pin = Pin(relay_pin, Pin.OUT)
        rl_on = 0
        relay = RelayControl(name=relay_name, _pin=relay_pin, on_value=rl_on, default=1-rl_on)
        relay.set_callback(self.relay_cb)
        self.relays[relay_name] = relay

        if self.mbus:

            self.mbus.sub("RC_{}".format(key), {"id": relay_name, "func": self.control_relay})

            self.mbus.pub({
                            "id": "TOPIC",
                            "msg": {"name": relay_name, "data": "set"}
                            })

            self.mbus.pub({
                            "id": "TOPIC",
                            "msg": {"name": relay_name, "data": "state"}
                            })


    def control_relay(self, key, msg):
        # print("------{} - {}".format(key, msg))
        if msg["name"] == "set":
            if msg["data"] == "ON":
                self.relays[key].on()
            if msg["data"] == "OFF":
                self.relays[key].off()

        if msg["name"] == "change":
            self.relays[key].change_state()


    def relay_cb(self, relay):
        
        if self.mbus:
            self.mbus.pub({
                            "id": relay.name,
                            "msg": {"name": "state", "data": relay.state, "retain": True}
                            })
 

