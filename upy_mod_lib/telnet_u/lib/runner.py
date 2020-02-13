from .core import TelnetServer

import logging
log = logging.getLogger("TELNET")
log.setLevel(logging.INFO)




class TelnetRunner:

    def __init__(self, mbus, umod, param="default"):

        self.mbus = mbus
        self.umod = umod

        self.telnet = TelnetServer()
        self.param = param
        mbus.sub_h("TELNET", "telnet/#", self.telnet_act)

    #telnet Actions
    def telnet_act(self, msg):
        log.debug("[TELNET-ACT]: set: {}".format(msg))

        if msg["id"] == "telnet/ctr":

            if msg["key"] == "start":
                self.telnet_param()
                self.telnet.start()

            if msg["key"] == "stop":
                self.telnet.stop()


    def telnet_param(self):

        telnet_cfg = self.umod.rec_sel("cfg_telnet", name="default")

        if len(telnet_cfg):
            log.debug("[TELNET-CFG]: set: {}".format(telnet_cfg))
            self.telnet.port = telnet_cfg[0]["port"]
            self.telnet.pswd = telnet_cfg[0]["pswd"]
