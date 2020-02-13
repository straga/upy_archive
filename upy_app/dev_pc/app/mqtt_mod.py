from mqtt_u.runner import MQTTClientRunner

try:
    from ucollections import OrderedDict
except Exception:
    from collections import OrderedDict

def init_db(umod):

    tb_name= "cfg_mqtt"
    tb_schema = OrderedDict([
        ("name", ""),
        ("type", ""),
        ("ip", ""),
        ("port", ""),
    ])

    umod.mod_add(tb_name, tb_schema, active="1", up="sta")


def init_act(_core):
    MQTTClientRunner(_core.mbus, _core.umod, _core.board)
    return _core

