from .core import MQTTClient

import logging
log = logging.getLogger("MQTT")
log.setLevel(logging.INFO)


class MQTTClientRunner:

    def __init__(self, mbus, umod, board):

        self.brk_name = "MQTT"
        self.umod = umod
        self.board = board

        self.mqtt = MQTTClient()


        # mod mbus
        self.mbus = mbus
        self.mbus.MQTT = self.MQTT
        self.mbus.sub_h("MQTT-TPC", "mqtt/#", self.mqtt_act)

    async def mqtt_param(self):

        # board_inf = await self.umod._by_id("cfg_board", self.board)
        board_inf = await self.umod.call_db("_by_id", "board_cfg", pkey=self.board)

        log.debug("Board : {}".format(board_inf))

        if board_inf:

            client_id = board_inf["client"]
            self.mqtt.client_id = client_id

            mqtt_host = await self.umod.call_db("_sel", "cfg_mqtt", type="default")

            if len(mqtt_host):
                self.mqtt.server = mqtt_host[0]["ip"]

                self.c_sub = "{}/{}".format(client_id, self.brk_name)
                self.c_pub = client_id


                self.mqtt.sbt = "{}/#".format(self.c_sub)
                self.mqtt.set_callback(self.mqtt_cb)

                self.mbus.sub_h("MQTT-ALL", "ALL", self.mbus_act)




    # MQTT Actions
    async def mqtt_act(self, _id, _key, _pld, _rt):
        log.debug("[MQTT-MBUS]: {},{},{},{} :: ACT".format(_id, _key, _pld, _rt))

        if _id == "mqtt/ctr":

            if _key == "start":
                await self.mqtt_param()
                self.mqtt.start()

            if _key == "stop":
                self.mqtt.stop()

            if _key == "restart":
                self.mqtt.stop()
                await self.mqtt_param()
                self.mqtt.start()



    # Publish from mqtt to mbus
    def mqtt_cb(self, topic, msg, retain):
        tpc_list = topic.rsplit(self.c_sub + "/", 1)
        self.mbus.pub_h(tpc_list[-1], msg, brk=self.brk_name, retain=retain)


    # Publish from mbus to mqtt
    def mbus_act(self, _id, _key, _pld, _rt):

        log.debug("[MQTT-MBUS]: _id:{}, _key:{}, _pld:{}, _rt:{} ->mqtt".format(_id, _key, _pld, _rt))

        #     tpc = msg["key"] in self.tpc

        if _id not in [self.brk_name, "private"]:

            val = {
                    "tp": "{}/{}/{}".format(self.c_pub, _id, _key),
                    "msg": _pld,
                    "rt": _rt
                   }
            self.mqtt.pub(val)


    # MQTT Broker for MBUS
    def MQTT(self, msg):
        log.debug("[brk MQTT]: {}".format(msg))
        msg["pld"] = msg["pld"].decode()
        return msg






