from push_u.runner import PushRunner

try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict


def init_db(umod):

    tb_name = "cfg_push"
    tb_schema = OrderedDict([
        ("name", ""),
        ("b_pin", ""),
        ("p_on", ""),
        ("p_mode", ""),
        ("p_pull", ""),
        ("ps_mode", ""),
        ("ps_pin", ""),
        ("value", ""),
    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="main")


def init_act(_core):
    PushRunner(_core.mbus, _core.umod)
    return _core








