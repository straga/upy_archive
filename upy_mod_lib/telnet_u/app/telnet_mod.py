from telnet_u.runner import TelnetRunner

try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict



def init_db(umod):

    tb_name = "cfg_telnet"
    tb_schema = OrderedDict([
        ("name", ""),
        ("port", ""),
        ("pswd", ""),
    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="ap")


def init_act(_core):
    TelnetRunner(_core.mbus, _core.umod)
    return _core