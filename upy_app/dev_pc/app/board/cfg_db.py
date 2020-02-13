
_name_board = "default"

def mod_debug():

    import logging
    log = logging.getLogger("PIN")
    log.setLevel(logging.INFO)

    log = logging.getLogger("FDB")
    log.setLevel(logging.INFO)

    log = logging.getLogger("MOD")
    log.setLevel(logging.INFO)

    log = logging.getLogger("MBUS")
    log.setLevel(logging.INFO)

    log = logging.getLogger("PUSH")
    log.setLevel(logging.INFO)

    log = logging.getLogger("Control")
    log.setLevel(logging.INFO)

    log = logging.getLogger("RELAY")
    log.setLevel(logging.INFO)

    pass


def push_board(umod):

    umod.call_cmd("_add", "board_cfg",
                     name="default",
                     board="pc_dev",
                     uid="2132323213",
                     client="dev/pc_dev",
                     init=0
                 )

    umod.call_cmd("_add", "board_mod", name="wifi", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="mqtt", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="ftp", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="pin", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="relay", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="push", active=1, status="")
    umod.call_cmd("_add", "board_mod", name="control", active=1, status="")


def push_data(umod):

    umod.call_cmd("_add", "cfg_mqtt",
                 name="local_1",
                 ip="192.168.100.236"
                 )

    umod.call_cmd("_add", "cfg_mqtt",
                 name="local_2",
                 type="default",
                 ip="192.168.197.141"
                 )

    umod.call_cmd("_add", "cfg_mqtt",
                 name="local_3",
                 ip="192.168.254.1"
                 )



    umod.call_cmd("_add", "cfg_wifi_sta",
                 name="demosta",
                 ssid="demosta",
                 passwd="demosta"
                 )



    umod.call_cmd("_add", "cfg_wifi_ap",
                 name="default",
                 essid="esp32_default",
                 channel=11,
                 hidden="false",
                 password="default",
                 authmode=3,
                 )


    umod.call_cmd("_add", "cfg_ftp",
                 name="default",
                 ip="",
                 port=25,
                 dport=26
                 )

    umod.call_cmd("_add", "board_pin", name="led_status", npin="emu", bpin=5)
    umod.call_cmd("_add", "board_pin", name="btn_1", npin="emu", bpin=4)
    umod.call_cmd("_add", "board_pin", name="relay_1", npin="emu", bpin=5)
    umod.call_cmd("_add", "board_pin", name="relay_2", npin="emu", bpin=6)
    umod.call_cmd("_add", "board_pin", name="i2c1_sdc", npin="emu", bpin=6)
    umod.call_cmd("_add", "board_pin", name="i2c1_sda", npin="emu", bpin=7)



    umod.call_cmd("_add", "cfg_relay",
                  name="relay_2",
                  b_pin="relay_2", p_on=1, p_def=0, p_mode="OUT",
                  r_mode="led", r_pin=None,
                  value="emu")


    umod.call_cmd("_add", "cfg_relay",
                  name="relay_1", b_pin="relay_1",
                  p_on=0, p_def=0, p_mode="OUT",
                  r_mode="led", r_pin=None,
                  value="emu")


    umod.call_cmd("_add", "cfg_push",
                  name="push_1", b_pin="btn_1",
                  p_on=1, p_mode="IN", p_pull="PULL_DOWN",
                  ps_mode="led", ps_pin=None,
                  value="emu")


    umod.call_cmd("_add", "cfg_push",
                  name="push_2", b_pin="btn_1",
                  p_on=1, p_mode="IN", p_pull="PULL_DOWN",
                  ps_mode="led", ps_pin=None,
                  value="emu")
