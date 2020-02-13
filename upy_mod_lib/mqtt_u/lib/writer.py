import logging
log = logging.getLogger("MQTT")
log.setLevel(logging.INFO)


async def u_awrite(writer, data, b=False):
    if not b:
        data = data.encode('utf-8')

    #micropython
    try:
        await writer.awrite(data)
    except Exception as e:
        log.debug("Error: write: {}".format(e))
        pass

async def u_aclose(writer):
    try:
        await writer.aclose()
    except Exception as e:
        log.debug("Error: write: {}".format(e))
        pass



def pc_aclose(writer):

    try:
        writer.close()
    except Exception as e:
        log.debug("Error: write: {}".format(e))
        pass


async def pc_awrite(writer, data, b=False):
    if not b:
        data = data.encode('utf-8')

    #PC

    try:
        writer.write(data)
        await writer.drain()
    except Exception as e:
        log.debug("Error1: wait_msg: {}".format(e))
        pass

