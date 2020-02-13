# Copyright (c) 2018 Viktor Vorobjov
import uasyncio as asyncio

import logging
log = logging.getLogger("HTTP_CLIENT")
log.setLevel(logging.DEBUG)
# log.setLevel(logging.INFO)


class ClientResponse:

    def __init__(self, reader):
        self.content = reader
        self.status = None
        self.headers = None

    async def read(self, sz=-1):
        return await self.content.read(sz)

    async def readexactly(self, sz):
        return await self.content.readexactly(sz)

    readexactly

    def __repr__(self):
        return "<ClientResponse %d %s>" % (self.status, self.headers)


async def request_raw(method, url):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto != "http:":
        raise ValueError("Unsupported protocol: " + proto)
    port = 80
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    log.debug("Host:{} Port:{}".format(host, port))

    reader, writer = await asyncio.open_connection(host, port)

    # Use protocol 1.0, because 1.1 always allows to use chunked transfer-encoding
    # But explicitly set Connection: close, even though this should be default for 1.0,
    # because some servers misbehave w/o it.

    query = "{} /{} HTTP/1.0\r\nHost: {}\r\nConnection: close\r\nUser-Agent: compat\r\n\r\n".format(method, path, host)
    log.debug("Query:{}".format(query))

    try:
        await writer.awrite(query.encode('latin-1'))
    except Exception as err:
        log.error(err)
        writer.aclose()

    # addr = writer.get_extra_info('peername')
    log.debug("board -> {}".format(host))

    return reader


async def request(method, url):
    redir_cnt = 0
    headers = []
    status = 0
    reader = False

    while redir_cnt < 2:
        reader = await request_raw(method, url)
        try:
            s_line = await reader.readline()
        except Exception as err:
            await reader.aclose()
            log.error("s_line: ".format(err))
            break

        if s_line != b"\r\n" and s_line != b"":
            s_line = s_line.split(None, 2)
            status = int(s_line[1])

        log.debug("board <-- Service:{}".format(s_line))

        while True:
            try:
                h_line = await reader.readline()
            except Exception as err:
                h_line = b""
                log.error("h_line: ".format(err))
                pass

            log.debug("board <-- Header:{}".format(h_line))

            if h_line == b"\r\n" or h_line == b"":
                break

            headers.append(h_line)

            if h_line.startswith(b"Location:"):
                url = h_line.rstrip().split(None, 1)[1].decode("latin-1")
                log.info("board <--> redirect ->:{}".format(url))


        if 301 <= status <= 303:
            redir_cnt += 1
            await reader.aclose()
            continue
        break

    if reader:
        resp = ClientResponse(reader)
        resp.status = status
        resp.headers = headers
        return resp

    return False
