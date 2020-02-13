from .core import FTPServer

import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)


class FTPRunner:

    def __init__(self, mbus, umod):

        self.mbus = mbus
        self.umod = umod

        self.ftp = FTPServer()
        self.param = "default"
        mbus.sub_h("FTP", "ftp/#", self.ftp_act)

    # FTP Actions
    async def ftp_act(self, _id, _key, _pld, _rt):
        log.debug("[ACT]: id: {}, key: {}, pld: {}, rt: {}".format(_id, _key, _pld, _rt))

        if _id == "ftp/ctr":

            if _key == "start":
                await self.ftp_param(_pld)
                self.ftp.start()


    async def ftp_param(self, addr):
        log.debug("addr: {}".format(addr))

        ftp_cfg = await self.umod.call_db("_sel", "cfg_ftp", name="default")

        log.debug("cfg: {},".format(ftp_cfg))
        if ftp_cfg:
            self.ftp.port = ftp_cfg[0]["port"]
            self.ftp.dport = ftp_cfg[0]["dport"]

        self.ftp.addr = addr
