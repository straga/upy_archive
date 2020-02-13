from telnetse import TelnetServer


class TelnetServerActivate:

    def __init__(self, mbus):
        self.telnet = TelnetServer()
        mbus.sub("telnetse", {"id": "WIFI", "func": self.telnet_activate})

    def telnet_activate(self, key, msg):
        if msg["name"] == "sta_ip" or msg["name"] == "ap_ip":
            self.telnet.start()
