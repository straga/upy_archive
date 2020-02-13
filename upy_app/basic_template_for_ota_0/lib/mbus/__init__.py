# Copyright (c) 2018 Viktor Vorobjov

import uasyncio as asyncio
from uasyncio.queues import Queue

import logging
log = logging.getLogger("MBUS")
log.setLevel(logging.INFO)



class MbusManager:

    def __init__(self):

        self.queue = Queue()
        self.msub = {}
        self.mpub = []
        self.run = False
        self.m_addr = "MQTT->"
        self.msg_sz = len(self.m_addr)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.consumer())
        loop.create_task(self.producer())
        self.run = True


    # consumer
    def sub(self, key, value):
        self.msub[key] = value

    async def consumer(self):
        log.debug("Consumer started")

        while True:
            message = await self.queue.get()
            if message:
                log.debug("Consumer get: {}".format(message))

                for key, value in self.msub.items():
                    func = value["func"]
                    sub_id = value["id"]



                    #mqtt trasport
                    msg_id = message["id"]
                    if msg_id[:self.msg_sz] == self.m_addr:
                        # not send to trasnport again
                        if key[:1] == "_" and sub_id == "ALL":
                            sub_id = "_ALL"
                        msg_id = msg_id[self.msg_sz:]



                    if sub_id == msg_id or sub_id == "ALL":
                        if sub_id == "ALL":
                            key_msg = msg_id
                        else:
                            key_msg = sub_id
                        func(key_msg, message["msg"])

            await asyncio.sleep(0.3)


    # producer
    def pub(self, value):
        self.mpub.append(value)


    async def producer(self):

        while True:
            if self.mpub:
                for value in self.mpub[:]:

                    bus_message = {
                        "id": value["id"],
                        "msg":  value["msg"]
                    }

                    await self.queue.put(bus_message)
                    self.mpub.remove(value)

            await asyncio.sleep(0.3)






    # async def producer(self, m_key, m_value):
    #
    #         if m_key:
    #             bus_message = {"type": m_key, "msg": m_value}
    #             await self.queue.put(bus_message)