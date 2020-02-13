
import sys
runnin_gpart_name = "./"

sys.path.append("{}".format(runnin_gpart_name))
sys.path.append("{}/{}".format(runnin_gpart_name, "lib"))
sys.path.append("{}/{}".format(runnin_gpart_name, "app"))


import logging

log = logging.getLogger('MAIN')
logging.basicConfig(level=logging.DEBUG)

import _thread
import asyncio

from mbus_u.core import MbusManager
from mod_u.core import ModManager


def print_mbus(*msg):
    print("MAIN: {}".format(msg))

def main():


    board_id = b"12321421232321"
    print(board_id)

    # AsyncIO
    loop = asyncio.get_event_loop()

    # _ = _thread.stack_size(10 * 1024)
    _thread.start_new_thread(loop.run_forever, ())

    # MBUS
    global g_mbus
    g_mbus = MbusManager()
    g_mbus.start()
    print("MBUS START")

    g_mbus.sub_h("MAIN", "ALL", print_mbus)

    # MOD
    global g_umod
    g_umod = ModManager("./u_db")
    print("MOD START")

    from board_mod import Activate as BoardActivate
    BoardActivate(g_mbus, g_umod, board_id)



    #atest.relays["pump_1"].change_state()
    #atest.relays["pump_1"].change_state(1)
    #atest.relays["dev/Local_PC/pump_1"].change_state(1)
    # mbus.pub({})
    # mbus_c.pub_h("Test", "wifi/status", "45")
    # mbus_c.pub_h("wifi/status", "45")
    # mbus_c.pub_h("wifi/status", "45", "MQTT")
    # mbus_c.pub_h("", "45", ")
    # mbus_c.pub_h("pump_1/set", "ON")

    # mbus.pub({"id": "ON_PUMP", "msg": {"name": "dev/Local_PC/pump_1/set", "data": "ON" }})





if __name__ == '__main__':

    print("MAIN")
    main()