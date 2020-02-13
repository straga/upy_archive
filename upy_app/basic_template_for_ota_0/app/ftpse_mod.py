from ftpse import FTPServer
import logging
log = logging.getLogger("FTPSE act")
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

class FTPServerActivate:

    def __init__(self, mbus):
        self.ftpse = FTPServer(port=25)
        mbus.sub("ftpse", {"id": "WIFI", "func": self.ftpse_activate})


    def ftpse_activate(self, key, msg):
        if msg["name"] == "sta_ip" or msg["name"] == "ap_ip":
            log.debug("MBUS FTPSE: {} , {}".format(key, msg))
            self.ftpse.run(msg["data"])

