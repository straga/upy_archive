# Copyright (c) 2018 Viktor Vorobjov
import network
import uasyncio as asyncio
from config import CONFIG


import logging
log = logging.getLogger("WIFI")
log.setLevel(logging.INFO)

class WifiManager:

    def __init__(self, file_ap=None, file_sta=None, mbus=None):

        self.status = {"ap": False, "sta": False}

        self.file_sta = file_sta
        self.file_ap = file_ap

        self.config = CONFIG()

        self.run = False

        self.mbus = mbus


    # @classmethod
    def accesspoint(self):
        return network.WLAN(network.AP_IF)

    # @classmethod
    def wlan(self):
        return network.WLAN(network.STA_IF)

    def start(self):
        loop = asyncio.get_event_loop()
        if not self.run:
            loop.create_task(self.run_wifi())
            log.info("Wifi Manager Started {}".format("!"))
            self.run = True
        return True



    async def run_wifi(self):

        while True:
            ip = self.wlan().ifconfig()[0]
            log.debug("STA IP {}".format(ip))

            if ip == "0.0.0.0":
                await self.ap_service(state="start")
                await self.sta_service()
            else:
                await self.ap_service(state="stop")

            await asyncio.sleep(20)


    async def sta_service(self):
        self.config.file = self.file_sta
        config_sta = self.config.load_config()
        log.debug("STA config {}".format(config_sta))

        if self.status["sta"]:
            self.change_status(if_type="sta", status=False, ip="0.0.0.0")

        if config_sta:

            self.wlan().active(True)

            while True:

                for key, value in config_sta.items():
                    self.wlan().connect(value["ssid"], value["paswd"])
                    await asyncio.sleep(15)

                    ip = self.wlan().ifconfig()[0]
                    if ip != "0.0.0.0":
                        self.change_status(if_type="sta", status=True, ip=ip)
                        break
                break
        else:
            await asyncio.sleep(30)

    async def ap_service(self, state=None):

        status = self.accesspoint().active()

        if state == "start" and not status:

            self.config.file = self.file_ap
            config_ap = self.config.load_config(get_key="ap")
            log.debug("AP config {}".format(config_ap))

            if config_ap:

                self.accesspoint().active(True)
                self.accesspoint().config(essid=config_ap["essid"])
                self.accesspoint().config(authmode=config_ap["authmode"],
                                          password=config_ap["password"],
                                          channel=config_ap["channel"])

                self.change_status(if_type="ap", status=True, ip=self.accesspoint().ifconfig()[0])

        elif state == "stop" and status:

            self.accesspoint().active(False)
            self.change_status(if_type="ap", status=False)

        await asyncio.sleep(1)

    def change_status(self, if_type=None, status=None, ip=None):

        log.debug("Status {} - {} - {}".format(if_type, status, ip ))

        self.status[if_type] = status
        if self.mbus:
            self.mbus.pub({
                            "id": "WIFI",
                            "msg": {"name": "{}_status".format(if_type), "data": status}
                            })

        if ip and self.mbus:
            self.mbus.pub({
                            "id": "WIFI",
                            "msg": {"name": "{}_ip".format(if_type), "data": ip}
                            })


    # async def change_status(self, if_type=None, status=None, ip=None):
    #
    #     log.debug("Status {} - {} - {}".format(if_type, status, ip ))
    #
    #     self.status[if_type] = status
    #     if self.mbus:
    #         await self.mbus.producer("WIFI", {"name": "{}_status".format(if_type), "data": status})
    #
    #     if ip and self.mbus:
    #         await self.mbus.producer("WIFI", {"name": "{}_ip".format(if_type), "data": ip})


# async def _scan(self):
#     scan = None
#     try:
#         scan = self.wlan().scan()
#     except:
#         pass
#     return scan

# scan = await self._scan()
#
# for ap in scan:
#     if ap[0].decode("utf-8") in config_sta.keys():
#         self.wlan().connect(ap[0].decode("utf-8"), config_sta[ap[0].decode("utf-8")])






