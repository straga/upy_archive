# Copyright (c) 2019 Viktor Vorobjov

try:
    import uos
    import utime
    import ujson
    from ucollections import OrderedDict

except Exception:

    import os as uos
    import time as utime
    from collections import OrderedDict
    import json as ujson
    pass

import logging
log = logging.getLogger("FDB")
log.setLevel(logging.INFO)

class DB:

    def __init__(self, name):
        self.name = name

    def connect(self):
        pass

    def close(self):
        pass


class Model:

    @classmethod
    def fname(cls, pkey):
        return "{}/{}/{}".format(cls.__db__.name, cls.__table__, pkey)

    @classmethod
    def fname_in(cls):
        return "{}/{}".format(cls.__db__.name, cls.__table__)


    @classmethod
    def list_dir(cls, path):
        try:
            return uos.listdir(path)
        except OSError as e:
            log.debug("LSDIR: {}".format(e))
            return []


    @classmethod
    def isfile(cls, file):
        try:
            if uos.stat(file)[6]: #size more 0
                return True
            else:
                return False
        except OSError as e:
            log.debug("LSFILE: {}".format(e))
            return False


    @classmethod
    def create_table(cls):
        cls.__fields__ = list(cls.__schema__.keys())

        for d in (cls.__db__.name, cls.fname_in()):
            if not cls.list_dir(d):
                try:
                    uos.mkdir(d)
                except OSError as e:
                    log.debug("MKDIR: {}, {}".format(e, d))
                    pass


    @classmethod
    def create(cls, **fields):
        pkey_field = cls.__fields__[0]
        for k, v in cls.__schema__.items():
            if k not in fields:
                default = v
                if callable(default):
                    default = default()
                fields[k] = default

        pkey = fields[pkey_field]
        exs = cls.isfile(cls.fname(pkey))

        log.debug("Exist:{}, file: {}".format(exs , cls.fname(pkey)))
        log.debug("create: fields:{}".format(ujson.dumps(fields)))

        if not exs:
            with open(cls.fname(pkey), "w") as f:
                f.write(ujson.dumps(fields))
            log.debug("create: pkey:{}".format(pkey))
            return pkey
        else:
            log.debug("exist: pkey:{}".format(pkey))
            return False


    @classmethod
    def get_id(cls, pkey):
        with open(cls.fname(pkey)) as f:
            return ujson.loads(f.read())



    @classmethod
    def update(cls, where, **fields):
        pkey_field = cls.__fields__[0]

        if len(where) == 1 and pkey_field in where:

            with open(cls.fname(where[pkey_field])) as f:
                data = ujson.loads(f.read())

            data.update(fields)

            with open(cls.fname(where[pkey_field]), "w") as f:
                f.write(ujson.dumps(data))

            return True



    @classmethod
    def scan(cls):
        for fname in cls.list_dir(cls.fname_in()):

            # log.debug("fname: {}".format(cls.fname(fname)))

            with open(cls.fname(fname)) as f:
                tb = f.read()
                if tb:
                    row = ujson.loads(tb)
                    yield row


    @classmethod
    def delete(cls, where):
        pkey_field = cls.__fields__[0]

        if len(where) == 1 and pkey_field in where:
            uos.remove(cls.fname(where[pkey_field]))
            return True


    @classmethod
    def select(cls, **fields):

        for v in cls.list_dir(cls.fname_in()):

            with open(cls.fname(v)) as f:
                tb = f.read()
                if tb:
                    row = ujson.loads(tb)

                    for k in cls.__fields__:
                        if k in fields and k in row:
                            if row[k] == fields[k]:
                                yield row


# if hasattr(utime, "localtime"):
#     def now():
#         return "%d-%02d-%02d%02d:%02d:%02d" % utime.localtime()[:6]
# else:
#     def now():
#         return str(int(utime.time()))

def now():
    return str(int(utime.time()))
