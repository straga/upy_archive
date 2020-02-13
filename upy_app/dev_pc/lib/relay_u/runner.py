from .core import RelayModel
from machine import Pin

from asyn.asyn import launch

import logging
log = logging.getLogger("RELAY")
log.setLevel(logging.INFO)

class RelayRunner:

    def __init__(self, mbus, umod):

        self.umod = umod
        self.mbus = mbus
        launch(self._activate_relay, "")
        self.mbus.sub_h("RELAY", "relay/#", self.relay_act)


    def _get_relay(self, cfg_relay):

        relay = RelayModel(cfg_relay, mbus=self.mbus, umod=self.umod)

        relay.relay_ctrl._pin = Pin(relay.r_pin, getattr(Pin, relay.p_mode))
        relay.relay_ctrl._value = relay.relay_ctrl._pin.value

        if relay.value == "emu":
            relay.relay_ctrl._pin._tb = "cfg_relay"
            relay.relay_ctrl._pin._name = relay.name
            relay.relay_ctrl._pin._umod = self.umod

        return relay


    async def _activate_relay(self):

        cfgs = await self.umod.call_db("_scan", "cfg_relay")

        for cfg_relay in cfgs:

            info_pin = await self.umod.call_db("_sel_one", "board_pin",  name=cfg_relay["b_pin"])

            if info_pin and info_pin["bpin"]:
                cfg_relay["r_pin"] = info_pin["bpin"]

                await self.umod.call_db("_upd", "cfg_relay", {"name": cfg_relay["name"]}, r_pin=info_pin["bpin"], value=info_pin["npin"])

                relay = self._get_relay(cfg_relay)

                log.debug("ADD: {}".format(relay.name))

                relay.relay_ctrl.change_state(relay.p_def)


    async def relay_act(self, _id, _key, _pld, _rt):
        log.debug("[ACT]: id: {}, key: {}, pld: {}, rt: {}".format(_id, _key, _pld, _rt))

        if _key == "set":

            rl_name = _id.split("relay/", 1)[-1]
            log.debug("rl_name: {}".format(rl_name))

            cfg_relay = await self.umod.call_db("_sel_one", "cfg_relay", name=rl_name)
            log.debug("cfg_relay: {}".format(cfg_relay))

            if cfg_relay:
                relay = self._get_relay(cfg_relay)

                if _pld == "ON":
                    relay.relay_ctrl.on()
                if _pld == "OFF":
                    relay.relay_ctrl.off()
                if _pld == "change":
                    relay.relay_ctrl.change_state()

