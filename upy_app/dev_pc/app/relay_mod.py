from relay_u.runner import RelayRunner

try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict


def init_db(umod):

    tb_name = "cfg_relay"
    tb_schema = OrderedDict([
        ("name", ""),
        ("b_pin", ""),
        ("p_on", ""),
        ("p_def", ""),
        ("p_mode", ""),
        ("r_mode", ""),
        ("r_pin", ""),
        ("value", ""),

    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="main")

def init_act(_core):
    RelayRunner(_core.mbus, _core.umod)
    return _core








