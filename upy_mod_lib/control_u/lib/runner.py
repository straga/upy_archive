import logging
log = logging.getLogger("Control")
log.setLevel(logging.INFO)

class ControlRunner:

    def __init__(self, _core):

        self.umod = _core.umod
        self.mbus = _core.mbus

        self.mbus.sub_h("CNTRL", "push/push_1/#", self.control_light)


    async def control_light(self, _id, _key, _pld, _rt):
        log.debug("[ACT]: id: {}, key: {}, pld: {}, rt: {}".format(_id, _key, _pld, _rt))

        if _key == "state" and _pld == "ON":
            self.mbus.pub_h("relay/relay_1/set", "change")
