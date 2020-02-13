from .core import PushModel
from machine import Pin

import logging
log = logging.getLogger("PUSH")
log.setLevel(logging.INFO)

from asyn.asyn import launch

class PushRunner:

    def __init__(self, mbus, umod):

        self.umod = umod
        self.mbus = mbus
        self.push = []
        launch(self._activate_push, "")



    def _get_push(self, cfg_push):

        push = PushModel(cfg_push, mbus=self.mbus, umod=self.umod)

        push._pin = Pin(push.ps_pin, getattr(Pin, push.p_mode), getattr(Pin, push.p_pull))
        push._value = push._pin.value

        if push.value == "emu":
            push._pin._tb = "cfg_push"
            push._pin._name = push.name
            push._pin._umod = self.umod

        return push


    async def _activate_push(self):

        cfg_list = await self.umod.call_db("_scan", "cfg_push")

        log.debug("push: {}".format(cfg_list))

        for cfg_push in cfg_list:

            info_pin = await self.umod.call_db("_sel_one", "board_pin",  name=cfg_push["b_pin"])

            log.debug("PIN: {}".format(info_pin))

            if info_pin and info_pin["bpin"]:
                cfg_push["ps_pin"] = info_pin["bpin"]

            #self._get_push(cfg_push)

            self.push.append(self._get_push(cfg_push))

        log.debug("OBJ: {}".format(self.push))
