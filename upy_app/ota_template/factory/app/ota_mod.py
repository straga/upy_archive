import httpse.client_ota as aiohttp
from ota_updater import Updater
import ujson as json
import uasyncio as asyncio
import logging
log = logging.getLogger("OTA-MOD")
log.setLevel(logging.INFO)

class OtaServerActivate:
    
    def __init__(self, mbus, board_name):
        self.ota = Updater()
        self.board = board_name
        self.run_ota = True

        mbus.sub("ota", {"id": "WIFI", "func": self.ota_activate})

    def ota_activate(self, key, msg):
        if msg["name"] == "sta_ip":
            self.start()

    async def run(self):

        # To Do: from config file
        #addr = "http://192.168.100.173"
        addr = "http://192.168.254.1"
        port = "8080"

        url = "{}:{}/updatemeta/{}".format(addr, port, self.board)

        log.info("Start Update: {}".format(url))

        while True:

            # Request
            try:
                resp = await aiohttp.request("GET", url)
            except Exception as e:
                log.error("Resp:{}".format(e))
                break
            log.debug("Resp:{}".format(resp))

            # Data Json
            try:
                data = await resp.read()
            except Exception as e:
                log.error("Data:{}".format(e))
                break
            log.debug("Data:{}".format(data))

            data_str = data.decode()
            try:
                metadata = json.loads(data_str)
            except Exception as e:
                log.error("Data:{}, Err: {}".format(data_str, e))
                break

            # Run Update
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            log.debug("Type: {}, Data: {}".format(type(metadata), metadata))

            if "update" in metadata and metadata["update"]:
                res_updater = await self.ota.update(metadata["update"])
                log.info("Update: {}".format(res_updater))
            break


    async def delay_run(self):
        await asyncio.sleep(60)

        if self.run_ota:
            loop = asyncio.get_event_loop()
            loop.create_task(self.run())


    def start(self, delay=True):

        loop = asyncio.get_event_loop()
        if delay:
            loop.create_task(self.delay_run())
        else:
            loop.create_task(self.run())
            self.run_ota = False