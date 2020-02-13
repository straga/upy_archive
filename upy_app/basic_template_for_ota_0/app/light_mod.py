


class LightControlActivate:

    def __init__(self, mbus=False):
        self.mbus = mbus

        btn = "btn_right"

        if self.mbus:
            self.mbus.sub("LC_{}".format(btn), {"id": btn, "func": self.control_light})



    def control_light(self, key, msg):

        light_1 = "light_1"
        light_2 = "light_2"

        if msg["name"] == "state" and msg["data"] == "ON":

            self.mbus.pub({
                "id": light_1,
                "msg": {"name": "change", "data": msg["data"]}
            })

            self.mbus.pub({
                "id": light_2,
                "msg": {"name": "change", "data": msg["data"]}
            })