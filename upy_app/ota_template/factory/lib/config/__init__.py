# Copyright (c) 2018 Viktor Vorobjov
try:
    import ujson as json
    import uos as os
except:
    import json
    import os
import logging
log = logging.getLogger("config")
log.setLevel(logging.INFO)


class CONFIG:

    def __init__(self, file=False):
        self.file = file

    def load_config(self, get_key=False):

        try:
            with open(self.file) as f:
                config = json.loads(f.read())

                if get_key and get_key in config.keys():
                    return config[get_key]
                elif not get_key:
                    return config

        except (OSError, ValueError):
            log.debug("Couldn't load file")
            return False

    def save_config(self, config):

        try:
            with open(self.file, "w") as f:
                f.write(json.dumps(config))
        except OSError:
            log.debug("Couldn't save file")
            return False
        return True

    def put_config(self, key, value):

        config = self.load_config()
        if not config:
            config = {}
        config[key] = value
        self.save_config(config)
