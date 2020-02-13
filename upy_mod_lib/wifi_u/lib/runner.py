from .wifi import AP, STA
from .actions import WIFIActions


import logging
log = logging.getLogger("WIFI")
log.setLevel(logging.DEBUG)

class WIFIRunner:

    def __init__(self, mbus, umod):
        self._status = False
        self.mbus = mbus
        self.umod = umod
        self.sta = STA(mbus, umod)
        self.sta.start()
        WIFIActions(mbus, umod)


