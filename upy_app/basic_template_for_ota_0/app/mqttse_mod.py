from mqttse import MQTTClient


class MQTTClientActivate:

    def __init__(self, mbus, client_id):

        self.mbus = mbus
        self.mqtt = MQTTClient(client_id)
        self.mqtt.server = "192.168.254.1"
        self.mqtt.set_callback(self.mqtt_sub_cb)

        mbus.sub("MQTTSE_WiFi", {"id": "WIFI", "func": self._mqtt_activate})

        mbus.sub("_MQTTSE_A", {"id": "ALL", "func": self._mqtt_pub})
        mbus.sub("MQTTSE_T", {"id": "TOPIC", "func": self._mqtt_topic})

    def _mqtt_topic(self, key, msg):

        t_n = "{}_{}".format(msg["name"], msg["data"])
        t_p = "{}/{}".format(msg["name"], msg["data"])

        self.mqtt.set_topic(t_n, t_p)


    def _mqtt_pub(self, key, msg):
        if key[:5] != "MQTT-":
            retain = False
            if type(msg["data"]) is dict and "retain" in msg["data"]:
                retain = msg["data"]["retain"]

            self.mqtt.to_mqtt_bus("{}_{}".format(key, msg["name"]), msg["data"], retain)


    def _mqtt_activate(self, key, msg):
        if msg["name"] == "sta_ip":
            self.mqtt.run()



    # # MQTT
    def mqtt_sub_cb(self, topic, msg):

        t_dec = topic.decode()
        m_dec = msg.decode()

        if self.mbus:
            t_sp = t_dec.split("/")
            if len(t_sp) >= 4:

                p_type = t_sp[2]
                p_name = t_sp[3]

                self.mbus.pub({
                                "id": "MQTT->{}".format(p_type),
                                "msg": {"name": p_name, "data": m_dec}
                                })
            else:
                self.mbus.pub({
                    "id": "MQTT--",
                    "msg": {"name": t_dec, "data": m_dec}
                })
