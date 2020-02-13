
import esp
from utime import sleep
from machine import Pin, reset

safe_pin = Pin(4, Pin.IN, Pin.PULL_DOWN)
print("Wait 5sec - Safe Mode")
sleep(5)
print("Pin State: {}".format(safe_pin.value()))
if safe_pin.value() == 1:
    led_pin = Pin(2, Pin.OUT)
    led_pin.value(1)
    esp.ota_set_bootpart("factory")
    reset()
sleep(5)

import uos
import sys


def bytecompare(a,b):
    if (len(a) != len(b)):
        return False

    for i in range(0, len(a)):
        if (a[i] != b[i]):
            return False
    return True


def get_running_part_name():
    part = {}
    part["factory"] = esp.partition_find_first(0, 0, None)
    part["ota_0"] = esp.partition_find_first(0, 16, None)
    part["ota_1"] = esp.partition_find_first(0, 17, None)
    curbootpart = esp.ota_get_running_partition()

    if part["factory"] and bytecompare(part["factory"][6], curbootpart):
        return "factory"
    if part["ota_0"] and bytecompare(part["ota_0"][6], curbootpart):
        return "ota_0"
    if part["ota_1"] and bytecompare(part["ota_1"][6], curbootpart):
        return "ota_1"
    return None


runnin_gpart_name = get_running_part_name()

print("Booting from partition {}".format(runnin_gpart_name))
pyversion = 'None'
try:
    with open("/{}/VERSION".format(runnin_gpart_name), "r") as f:
        pyversion = f.read()
except:
    pass
print("Version hash: {}".format(pyversion.strip()))

sys.path.append("/{}".format(runnin_gpart_name))
sys.path.append("/{}/{}".format(runnin_gpart_name, "lib"))
sys.path.append("/{}/{}".format(runnin_gpart_name, "app"))
uos.chdir("/{}".format(runnin_gpart_name))
