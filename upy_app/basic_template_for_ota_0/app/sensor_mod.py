

from si7021 import SI7021
from bmp180 import BMP180


class SI7021ControlActivate:

    def __init__(self, mbus=None, i2c=False):
        self.mbus = mbus

        s_si = SI7021(i2c)
        s_si.read_delay = 300
        s_si.sensor_detect()
        s_si.start()
        s_si.name = "si"

        if self.mbus:

            self.mbus.pub({
                "id": "TOPIC",
                "msg": {"name": s_si.name, "data": "tem"}
            })

            self.mbus.pub({
                "id": "TOPIC",
                "msg": {"name": s_si.name, "data": "hum"}
            })


        s_si.set_callback(self.s_si_cb)

    def s_si_cb(self, si):

        if self.mbus:

            self.mbus.pub({
                "id": si.name,
                "msg": {"name": "tem", "data": si.temperature}
            })

            self.mbus.pub({
                "id": si.name,
                "msg": {"name": "hum", "data": si.humidity}
            })

class BMP180ControlActivate:

    def __init__(self, mbus=None, i2c=False):
        self.mbus = mbus

        s_bmp = BMP180(i2c)
        s_bmp.read_delay = 300
        s_bmp.sensor_detect()
        s_bmp.start()
        s_bmp.name = "bmp"

        if self.mbus:

            self.mbus.pub({
                "id": "TOPIC",
                "msg": {"name": s_bmp.name, "data": "tem"}
            })

            self.mbus.pub({
                "id": "TOPIC",
                "msg": {"name": s_bmp.name, "data": "pres"}
            })

            self.mbus.pub({
                "id": "TOPIC",
                "msg": {"name": s_bmp.name, "data": "alt"}
            })

        s_bmp.set_callback(self.s_bmp_cb)

    def s_bmp_cb(self, bmp):

        if self.mbus:

            self.mbus.pub({
                "id": bmp.name,
                "msg": {"name": "tem", "data": bmp.temperature}
            })

            self.mbus.pub({
                "id": bmp.name,
                "msg": {"name": "pres", "data": round(bmp.pressure*0.0075, 2)}
            })

            self.mbus.pub({
                "id": bmp.name,
                "msg": {"name": "alt", "data": bmp.altitude}
            })


