# Copyright (c) 2019 Viktor Vorobjov

try:
    import uasyncio as asyncio
    import ustruct as struct
    from .writer import u_awrite as _awrite
    from .writer import u_aclose as _aclose
except Exception:
    import asyncio
    import struct
    from .writer import pc_awrite as _awrite
    from .writer import pc_aclose as _aclose
    pass

import logging
log = logging.getLogger("MQTT")
log.setLevel(logging.INFO)


from .message import MQTTMessage


class MQTTClient:

    class Message(MQTTMessage):
        pass

    def __init__(self, client_id="", server=None, port=1883, keepalive=0, _ping_interval=60):

        self.client_id = client_id
        self.server = server
        self.port = port
        self.keepalive = keepalive
        self._run = False
        self.proto_name = b'MQTT'
        self.proto_ver = 4  #MQTTv311 = 4
        self._broker = None
        self._open = False
        self._reader = None
        self._writer = None
        self.open = 0
        self.pid = 0
        self.cb = None
        self._ping_interval = _ping_interval
        self._ping = 0
        self.sbt = None
        self.mpub = []





    def _unpack(self, data, pp="!B"):
        _unpk = struct.unpack(pp, data)
        return _unpk[0]


    def pack_variable_byte_integer(self, value):
        remaining_bytes = bytearray()
        while True:
            value, b = divmod(value, 128)
            if value > 0:
                b |= 0x80
            remaining_bytes.extend(struct.pack('!B', b))
            if value <= 0:
                break
        return remaining_bytes


    def pack_utf8(self, packet=bytearray(), data=''):

        if isinstance(data, str):
            data = data.encode('utf-8')
        packet.extend(struct.pack("!H", len(data)))
        packet.extend(data)
        return packet


    def bld_sm_pkg(self, command):
        return struct.pack('!BB', command, 0)



    async def awrite(self, writer, data, b=False):
        await _awrite(writer, data, b)

    async def _read_packet(self):
        remaining_count = []
        remaining_length = 0
        remaining_mult = 1

        while True:
            byte, = struct.unpack("!B", await self._reader.read(1))
            remaining_count.append(byte)

            if len(remaining_count) > 4:
                log.warning('[MQTT ERR PROTO] RECV MORE THAN 4 bytes for remaining length.')
                return None

            remaining_length += (byte & 127) * remaining_mult
            remaining_mult *= 128

            if byte & 128 == 0:
                break

        packet = b''
        while remaining_length > 0:
            chunk = await self._reader.read(remaining_length)
            remaining_length -= len(chunk)
            packet += chunk

        return packet


    async def close(self):

        self.open = 0
        self._broker = 0
        self._reader = False

        try:
            await _aclose(self._writer)
            self._writer = False
        except Exception as e:
            log.debug("Error: close: {}".format(e))
            pass

        log.debug("Connect Close{}")

        await asyncio.sleep(1)

    def set_callback(self, f):
        self.cb = f



    async def _heandler(self, m_type, m_raw):

        #CONNACK 0x20:  # dec 32
        if m_type == 0x20:
            code = 1
            self._broker = 0

            try:
                (flags, code) = struct.unpack("!BB", m_raw)
                log.debug('[CONNACK] flags: %s, code: %s', hex(flags), hex(code))
            except Exception as e:
                log.debug('[CONNACK] : {}'.format(e))
                pass

            # if return code not 0, something wrong, else #subscipe to topic
            if not code:
                log.info('Connected')
                self.open = 1
                self._broker = 1
                await self._subscribe()
            else:
                log.info('Disconnected')
                await self.close()




        #SUBACK 0x90 # dec 144
        elif m_type == 0x90:

            pack_format = "!H" + str(len(m_raw) - 2) + 's'
            (mid, packet) = struct.unpack(pack_format, m_raw)
            pack_format = "!" + "B" * len(packet)
            get_qos = struct.unpack(pack_format, packet)

            log.debug('[SUBACK] mid: {} q: {}'.format(mid, get_qos))
            if get_qos[0] == 0:  # 0x00 - Success - Maximum QoS 0 , 0x80 - Failure
                log.info('[SUBACK] mid: {}'.format(mid))
                self._ping = 0

        #PUBLISH 0x30, 0x31 # _handle_publish_packet , retain and not retain
        elif m_type in [0x30, 0x31]:

            retain = m_type & 0x01

            #format
            try:
                pack_format = "!H" + str(len(m_raw) - 2) + 's'
                (slen, packet) = struct.unpack(pack_format, m_raw)
                pack_format = '!' + str(slen) + 's' + str(len(packet) - slen) + 's'
            except Exception as exc:
                log.warning('[ERR pack format] {}'.format(exc))
                return
            #message
            try:
                (topic, packet) = struct.unpack(pack_format, packet)
            except Exception as exc:
                log.warning('[ERR unpack] {}'.format(exc))
                return

            #topic
            if not topic:
                log.warning('[ERR PROTO] topic name is empty')
                return

            try:
                print_topic = topic.decode('utf-8')
            except UnicodeDecodeError as exc:
                log.warning('[INVALID CHARACTER IN TOPIC] {}'.format(topic))
                print_topic = topic

            if self.cb:
                self.cb(print_topic, packet, retain)

        #PINGRESP 0xD0 # dec 208
        elif m_type == 0xD0:
            log.debug('[PING PINGRESP]')
            self._ping = 0


    async def _ping_msg(self):

        while self._run:

            if self._broker:

                command = 0xC0 #11000000 PINGREQ
                packet = self.bld_sm_pkg(command)
                await self.awrite(self._writer, packet, True)

            log.debug("[PING] {}, brocker: {}".format(self._ping, self._broker))

            if self._ping > 3:
                await self.close()


            self._ping += 1


            await asyncio.sleep(self._ping_interval)



    def newpid(self):
        return self.pid + 1 if self.pid < 65535 else 1

    async def subscribe(self, topic, qos=0):

        self.newpid()
        command = 0x80 #10000000
        command = command | 0 << 3 | 0 << 2 | 1 << 1 | 0 << 0 # + 0010

        remaining_length = 2
        remaining_length += 2 + len(topic) + 1

        packet = bytearray()
        packet.append(command)
        packet.extend(self.pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H", self.pid))
        packet = self.pack_utf8(packet, topic)

        subscribe_options = 0 << 3 | 0 << 2 | 0 << 1 | qos << 0
        #subscribe_options = retain_handling_options << 4 | retain_as_published << 3 | no_local << 2 | qos - 2.3.1 Packet Identifier
        packet.append(subscribe_options)

        log.debug("[SUBSCRIBE] topic: {} ,packet: {}".format(topic, packet))

        await self.awrite(self._writer, packet, True)


    async def _subscribe(self):
        log.info('[SUB TPC] : {}'.format(self.sbt))
        if self.sbt:
            await self.subscribe(self.sbt)



    def pub(self, value):
        self.mpub.append(value)


    async def publish(self, msg):

        command = 0x30  # 00110000
        command = command | 0 << 3 | (msg.qos << 1) | msg.retain << 0
        packet = bytearray()
        packet.append(command)
        remaining_length = 2 + len(msg.topic) + msg.pld_size
        packet.extend(self.pack_variable_byte_integer(remaining_length))
        packet = self.pack_utf8(packet, msg.topic)
        packet.extend(msg.pld)

        log.debug("[PUBLISH] topic: {} , msg: {} ,packet: {}".format(msg.topic, msg.pld, packet))

        await self.awrite(self._writer, packet, True)

    async def _publish(self):

        while self._run:
            while len(self.mpub) > 0:
                val = self.mpub.pop(0)
                if self._broker:
                    msg = MQTTClient.Message(val["tp"], val["msg"], val["rt"] if "rt" in val else False)
                    await self.publish(msg)

            await asyncio.sleep(0.3)


    async def _connect_to(self, clean):


        await self.close()

        try:
            log.info("[CONNECT] Server:{} Port:{}".format(self.server, self.port))
            self._reader, self._writer = await asyncio.open_connection(self.server, self.port)
            loop = asyncio.get_event_loop()
            loop.create_task(self._wait_msg())
            log.info("Connect Open")
        except Exception as e:
            log.debug("ERROR open connect: {}".format(e))
            return


        # MQTT Commands CONNECT
        command = 0x10
        remaining_length = 2 + len(self.proto_name) + 1 + 1 + 2 + 2 + len(self.client_id)

        connect_flags = 0
        if clean:
            connect_flags |= 0x02 #clean session


        packet = bytearray()
        packet.append(command)

        packet.extend(self.pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H" + str(len(self.proto_name)) + "sBBH",
                                  len(self.proto_name),
                                  self.proto_name,
                                  self.proto_ver,
                                  connect_flags,
                                  self.keepalive))

        packet = self.pack_utf8(packet, self.client_id)
        await self.awrite(self._writer, packet, True)




    async def _connect(self, clean=True):

        while self._run:

            if self.open == 0:
                await self._connect_to(clean)
                log.debug("Try CONNECT to MQTT")

            await asyncio.sleep(5.0)



    async def _wait_msg(self):

        while self._reader:
            try:
                log.debug("_msg_start: wait_msg: {}")
                byte = await self._reader.read(1)
                m_type = self._unpack(byte)
                m_raw = await self._read_packet()
                await self._heandler(m_type, m_raw)
                log.debug("_msg_end: wait_msg: {}".format(m_raw))
            except Exception as e:
                log.debug("Error1: wait_msg: {}".format(e))
                pass

            await asyncio.sleep(0.3)



    def start(self):

        if not self._run and self.server:
            self._run = True

            loop = asyncio.get_event_loop()
            loop.create_task(self._connect())
            # loop.create_task(self._wait_msg())
            loop.create_task(self._publish())
            loop.create_task(self._ping_msg())

            log.info("Coonect to = {}:{}".format(self.server, self.port))

    def stop(self):
        self._run = False
        loop = asyncio.get_event_loop()
        loop.create_task(self.close())








