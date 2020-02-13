
from collections import OrderedDict
import asyncio as asyncio
from wifi_u.actions import WIFIActions


def init_db(umod):


    tb_name= "cfg_wifi_sta"
    tb_schema = OrderedDict([
        ("name", ""),
        ("ssid", ""),
        ("passwd", ""),
    ])

    umod.mod_add(tb_name, tb_schema)

    tb_name= "cfg_wifi_ap"
    tb_schema = OrderedDict([
        ("name", ""),
        ("essid", ""),
        ("channel", ""),
        ("password", ""),
        ("authmode", ""),
    ])

    umod.mod_add(tb_name, tb_schema)


def init_act(_core):

    WIFIActions(_core.mbus, _core.umod)

    loop = asyncio.get_event_loop()
    loop.create_task(run_wifi(_core.mbus))

    return _core

async  def run_wifi(mbus):
    await asyncio.sleep(5)
    mbus.pub_h("WIFI/sta/ip/set", "127.0.0.1")
