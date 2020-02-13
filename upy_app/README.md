
# How to ... .
put in vfs:


    /factory/[files from ota_template/factory]
    /ota_0/[file from basic_template_for_ota_0] or leave default from [ota_template/ota_0]
    /boot.py

When board boot, select what base folder: dependence from partions("factory" or "ota_0")


ota_template/boot.py:
    --detect safe mode, if PIN(4) pull_UP, select factory partition and reboot.

app/config: configure wifi.

In factory partion, delay 60 sec for autoupdate from OTA server. You can stop auto update, connect repl or Telnet:
~#: import main
~#: ota_act.run_ota = False


In the file ota_mod.py, change ota server.
        addr = "http://192.168.10.113"
        port = "8080"



use uasyncio for async tasks. Non blocking, for asyncio use separate thread.
Folder from lib: compile in the mpy or put their in own firmware.