import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)


#micropython
async def u_awrite(writer, data, b=False):

    if not b:
        data = data.encode('utf-8')

    try:
        await writer.awrite(data)
    except Exception as e:
        log.debug("Error: write: {}".format(e))
        pass


async def u_aclose(writer):
    try:
        await writer.aclose()
    except Exception as e:
        log.debug("close: {}".format(e))
        pass

#upy
async def pc_aclose(writer):
    try:
        await writer.close()
    except Exception as e:
        log.debug("close: {}".format(e))
        pass


async def pc_awrite(writer, data, b=False):
    if not b:
        data = data.encode('utf-8')

    try:
        writer.write(data)
        await writer.drain()
    except Exception as e:
        log.debug("Error1: awrite: {}".format(e))
        pass

