


class PumpControlActivate:

    def __init__(self, mbus=False):
        self.mbus = mbus

        btn = "btn_left"
        self.pump = "pump_1"

        if self.mbus:
            self.mbus.sub("PC_{}".format(self.pump), {"id": btn, "func": self.control_pump})



    def control_pump(self, key, msg):

        if msg["name"] == "state" and msg["data"] == "ON":

                self.mbus.pub({
                                "id": self.pump,
                                "msg": {"name": "change", "data": msg["data"]}
                                })