from wifi import WifiManager
# import logging
# log = logging.getLogger("WIFI")
# log.setLevel(logging.DEBUG)


class WiFiActivate:

    def __init__(self, mbus):
        wifi = WifiManager("app/config/network_ap.json", "app/config/network_sta.json", mbus)
        wifi.start()
