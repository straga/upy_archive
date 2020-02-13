from wifi_u.runner import WIFIRunner
from ucollections import OrderedDict

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
    WIFIRunner(_core.mbus, _core.umod)
    return _core

