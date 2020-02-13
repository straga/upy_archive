
print("RUN MAIN FROM FACTORY")

from machine import unique_id, reset
from sys import platform
import ubinascii
import _thread

import uasyncio as asyncio

import logging
log = logging.getLogger("MAIN")
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)


from mbus import MbusManager
# log = logging.getLogger("MBUS")
# log.setLevel(logging.DEBUG)

from wifi_mod import WiFiActivate
from ftpse_mod import FTPServerActivate
from telnetse_mod import TelnetServerActivate

from ota_mod import OtaServerActivate

board_id = ubinascii.hexlify(unique_id())
board_name = "{}_{}".format(platform, board_id.decode())

def reboot(part):
    if part:
        import esp
        esp.ota_set_bootpart(part)
    reset()



def main():

    log.info(board_name)

    # Core
    mbus = MbusManager()
    mbus.start()

    WiFiActivate(mbus)
    FTPServerActivate(mbus)
    TelnetServerActivate(mbus)

    # OTA
    global ota_act
    ota_act = OtaServerActivate(mbus, board_name)

    # AsyncIO
    loop = asyncio.get_event_loop()

    # Tread
    _ = _thread.stack_size(8 * 1024)
    _thread.start_new_thread(loop.run_forever, ())


if __name__ == '__main__':

    print("MAIN")
    main()

