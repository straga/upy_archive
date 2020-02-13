from relay_control import RelayControl
from machine import Pin

import uasyncio as asyncio

class HeartbeatActivate:

    def __init__(self, mbus):

        led_pin = 2

        led_name = "LED_{}_HEARTBEAT".format(led_pin)
        led_pin = Pin(led_pin, Pin.OUT)
        self.led = RelayControl(name=led_name, _pin=led_pin, on_value=1, default=1)
        mbus.sub(led_name, {"id": "WIFI", "func": self.control_heartbeat})

        self.on_ms = 500
        self.off_ms = 5000

        # uasyncio
        loop = asyncio.get_event_loop()
        loop.create_task(self._led_blink())

        
    def control_heartbeat(self, key, msg):

        if msg["name"] == "ap_status":
            if msg["data"]:
                self.on_ms = 500
                self.off_ms = 1000

        elif msg["name"] == "sta_status":
            if msg["data"]:
                self.on_ms = 500
                self.off_ms = 10000


    async def _led_blink(self):

        while True:
            self.led.on()
            await asyncio.sleep_ms(self.on_ms)
            self.led.off()
            await asyncio.sleep_ms(self.off_ms)
