import logging
log = logging.getLogger("MQTT-MSG")
log.setLevel(logging.INFO)

try:
    import ujson as json
except Exception:
    import json
    pass

class MQTTMessage:
    def __init__(self, topic, pld, retain=False):
        self.topic = topic
        self.qos = 0
        self.retain = retain

        log.debug("[MSG]: {}, type: {}".format(pld, type(pld)))

        if isinstance(pld, (list, tuple, dict)):
            pld = json.dumps(pld)

        if isinstance(pld, (int, float, bool)):
            self.pld = str(pld).encode('ascii')
        elif isinstance(pld, str):
            self.pld = pld.encode('utf-8')
        elif pld is None or not isinstance(pld, bytes):
            self.pld = b''
        else:
            self.pld = pld

        log.debug("[MSG]: {}, type: {}".format(self.pld, type(self.pld)))

        try:
            self.pld_size = len(self.pld)
        except Exception as e:
            log.warning('[INVALID TYPE MSG] {}'.format(self.pld))
            self.pld = b''
            self.pld_size = len(self.pld)
            pass
