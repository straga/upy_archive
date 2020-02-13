# Copyright (c) 2018 Viktor Vorobjov
import logging
import uos
import uerrno
import uasyncio as asyncio
from . import FTPServer


log = logging.getLogger("ftpse")
log.setLevel(logging.INFO)

class FTPServerActive(FTPServer):

    async def send_data(self, type):

        log.debug("SEND Type: {}".format(type))
        log.debug("SEND Transfer: {}".format(self.transfer))


        if type is "passive":
            self.start = True
            while self.start:
                #wait 100ms for next check start. Lite =100, Hard = 0
                await asyncio.sleep_ms(100)

        if type is "active":
            log.info("Active: connecting to -> %s %d" % (self.data_ip, self.data_port))
            reader, writer = await asyncio.open_connection(self.data_ip, self.data_port)

            if self.transfer is "LIST":
                log.debug("s1. List Dir")
                await self.send_list_data(writer)

            if self.transfer is "SEND":
                log.debug("s1. Send File")
                await self.send_file_data(writer)

            if self.transfer is "SAVE":
                log.debug("s1. Save File")
                await self.save_file_data(reader)


            await writer.aclose()


        log.debug("s3. Send Data Done")
        return True

    async def PORT(self, stream, argument):
        argument = argument.split(',')
        self.data_ip = '.'.join(argument[:4])
        self.data_port = (int(argument[4])<<8)+int(argument[5])
        self.data_addr = (self.data_ip, self.data_port)
        log.info("got the port {}".format(self.data_addr))
        # await stream.awrite("220 Got the port.\r\n")
        await stream.awrite("200 OK.\r\n")
        self.con_type = "active"
        return True