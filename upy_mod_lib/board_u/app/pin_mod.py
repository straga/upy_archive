
try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict


def init_db(umod):

    tb_name = "board_pin"
    tb_schema = OrderedDict([
        ("name", ""),
        ("npin", ""),
        ("bpin", "")
    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="main")


def init_act(_core):
    return _core








