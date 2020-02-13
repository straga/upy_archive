from ftp_u.runner import FTPRunner

try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict


def init_db(umod):

    tb_name = "cfg_ftp"
    tb_schema = OrderedDict([
        ("name", ""),
        ("ip", ""),
        ("port", ""),
        ("dport", ""),
    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="ap")


def init_act(_core):
    FTPRunner(_core.mbus, _core.umod)
    return _core








