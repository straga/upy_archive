try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio
    pass

class WIFIActions:

    def __init__(self, mbus, umod):
        self.mbus = mbus
        self.umod = umod
        mbus.sub_h("WIFI-ACT", "WIFI/#", self.mod_ctrl)


    def mod_str(self, mods, up, pld):
        for mod in mods:
            if mod["active"] == "1" and mod["up"] in up:
                mod_name = mod["name"].split("cfg_", 1)
                self.mbus.pub_h("{}/ctr/start".format(mod_name[-1]), pld)


    def mod_stp(self, mods, up, pld):
        for mod in mods:
            if mod["active"] == "1" and mod["up"] in up:
                mod_name = mod["name"].split("cfg_", 1)
                self.mbus.pub_h("{}/ctr/stop".format(mod_name[-1]), pld)



    async def mod_ctrl(self, _id, _key, _pld, _rt):

        mods = await self.umod.call_db("_scan", "modules")

        if mods:

            if _id == "WIFI/sta/ip" and _key == "set":
                self.mod_str(mods, ["sta", "ap"], _pld)

            if _id == "WIFI/ap/is" and _key == "set":
                self.mod_str(mods, ["ap"], _pld)

            if _id == "WIFI/sta/ip" and _key == "clr":
                self.mod_stp(mods, ["sta"], _pld)