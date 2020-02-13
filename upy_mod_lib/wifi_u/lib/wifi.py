# import network
# import uasyncio as asyncio

import network
import uasyncio as asyncio

import logging
log = logging.getLogger("WIFI")
log.setLevel(logging.INFO)


class AP:
    def __init__(self):
        # self.ap = network.WLAN(network.AP_IF)
        # self.ap.active(True)
        pass


class STA:
    def __init__(self, mbus, umod):

        self._run = False
        self.mbus = mbus
        self.umod = umod

        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self._loss = 0
        self.sta_ip = None
        self._conf = None



    async def _connect(self):

        try:
            res = self.sta.scan()
        except Exception as e:
            print("WiFi err: {}".format(e))
            return

        ap_names = []
        for ap in res:
            ap_names.append(ap[0].decode())

        log.debug("ap_names: {}".format(ap_names))
        if ap_names and self._conf:
            for ap_c in self._conf:
                if ap_c["ssid"] in ap_names:
                    self.sta.connect(ap_c["ssid"], ap_c["passwd"])
                    await asyncio.sleep(15)



    async def _keepalive(self):


        while self._run:

            if self.sta.isconnected():
                self._loss = 0
                sleep = 10
                ip = self.sta.ifconfig()[0]
                self._conf = None

                if ip != self.sta_ip:
                    self.sta_ip = ip
                    self.mbus.pub_h("WIFI/sta/ip/set", self.sta_ip)

            else:
                self._loss += 1
                sleep = 1

            if self._loss > 10:

                self.sta.disconnect()
                self._loss = 0
                self._conf = await self.umod.call_db("_scan", "cfg_wifi_sta")

                if self.sta_ip is not None:
                    self.sta_ip = None
                    self.mbus.pub_h("WIFI/sta/ip/clr", self.sta_ip)
                    # log.debug("Active: {}".format(self._loss))


                await asyncio.wait_for(self._connect(), 20)



            await asyncio.sleep(sleep)

    def start(self):

        if not self._run:
            self._run = True

            loop = asyncio.get_event_loop()
            loop.create_task(self._keepalive())


    def stop(self):
        self._run = False
        self._conf = None
