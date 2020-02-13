# Copyright (c) 2018 Viktor Vorobjov
import upip_utarfile as utar
import os
import sys
import machine
import esp
import gc
import ubinascii
import hashlib
import json
# import urequests as requests
import httpse.client_ota as aiohttp

import logging
log = logging.getLogger("OTA")
#log.setLevel(logging.DEBUG)
log.setLevel(logging.DEBUG)

def byte_compare(a,b):


    if (len(a) != len(b)):
        return False

    for i in range(0, len(a)):
        if (a[i] != b[i]):
            return False
    return True


def copy_file_obj(src, dest, length=512):
    if hasattr(src, "readinto"):
        buf = bytearray(length)
        while True:
            sz = src.readinto(buf)
            if not sz:
                break
            if sz == length:
                dest.write(buf)
            else:
                b = memoryview(buf)[:sz]
                dest.write(b)
    else:
        while True:
            buf = src.read(length)
            if not buf:
                break
            dest.write(buf)

def copy_file(src, dest, length=512):
    with open(src, "rb") as fsrc:
        with open(dest, "wb") as fdest:
            while True:
                buf = fsrc.read(length)
                if not buf:
                    return
                fdest.write(buf)

def deep_copy_folder(src, dest):
    for f in os.ilistdir(src):
        psrc = "{}/{}".format(src, f[0])
        pdest = "{}/{}".format(dest, f[0])
        if f[1] == 0x4000:
            try:
                os.mkdir(pdest)
            except:
                pass
            deep_copy_folder(psrc, pdest)
        else:
            copy_file(psrc, pdest)

def deep_delete_folder(path):
    try:
        os.ilistdir(path)
    except:
        return

    for f in os.ilistdir(path):
        ppath = "{}/{}".format(path, f[0])
        if f[1] == 0x4000:
            deep_delete_folder(ppath)
            try:
                os.rmdir(ppath)
            except:
                pass
        else:
            try:
                os.remove(ppath)
            except:
                pass


    try:
        os.rmdir(path)
    except:
        pass

class Updater(object):
    """Handles OTA updates"""

    SEC_SIZE = 4096
    CHUNK_SIZE = 512
    TAR_PATH = "/update.tar"

    def __init__(self):

        self.partitions = {}
        self.partitions["factory"] = esp.partition_find_first(0, 0, None)
        self.partitions["ota_0"] = esp.partition_find_first(0, 16, None)
        self.partitions["ota_1"] = esp.partition_find_first(0, 17, None)
        self.boot_partition = esp.ota_get_running_partition()
        self.next_boot_partition = None
        self.cur_boot_partition = None
        self.next_boot_part_base_sec = None

        if self.partitions["factory"] and  byte_compare(self.partitions["factory"][6], self.boot_partition):
            if self.partitions["factory"] and self.partitions["ota_0"]:
                self.next_boot_partition = "ota_0"
                self.cur_boot_partition = "factory"

        if self.partitions["ota_0"] and byte_compare(self.partitions["ota_0"][6], self.boot_partition):
            if self.partitions["ota_1"] and self.partitions["ota_0"]:
                self.next_boot_partition = "ota_1"
                self.cur_boot_partition = "ota_0"

        if self.partitions["ota_1"] and  byte_compare(self.partitions["ota_1"][6], self.boot_partition):
            if self.partitions["ota_0"] and self.partitions["ota_1"]:
                self.next_boot_partition = "ota_0"
                self.cur_boot_partition = "ota_1"

        if self.next_boot_partition:
            self.next_boot_part_base_sec = self.partitions[self.next_boot_partition][2] // 4096
        else:
            log.error("Unsupported boot partition {}".format(self.boot_partition))

        log.info("Boot partition {}".format(self.boot_partition))
        for partition in self.partitions:
            log.info("Partition: {} - {}".format(partition, self.partitions[partition]))

        log.debug("Next Boot Partition {}".format(self.next_boot_partition))
        log.debug("Cur Boot Partition {}".format(self.cur_boot_partition))
        log.debug("Next boot part base sec {}".format(self.next_boot_part_base_sec))


    async def update(self, metadata):
        gc.collect()
        if self.check_signature(metadata):


            if "partition" in metadata:
                log.info('Starting partition update')

                url = metadata["partition"]["url"]
                size = metadata["partition"]["size"]
                hash = metadata["partition"]["hash"]
                log.debug('url: {}, size: {}, hash: {}'.format(url, size, hash))

                f_id = 0
                download_file = await self.download_chunk(url, size, 0, file=None)

                if not download_file:
                    return False

                if not self.check_partition(metadata["partition"]["hash"], metadata["partition"]["size"]):
                    self.delete_partition()
                    log.debug('Partion Delete')
                    return False
            else:
                self.copy_partition()


            if "vfs" in metadata:
                log.info('Starting vfs update')
                url = metadata["vfs"]["url"]
                size = metadata["vfs"]["size"]
                hash = metadata["vfs"]["hash"]
                log.debug('url: {}, size: {}, hash: {}'.format(url, size, hash))

                file = self.write_file(self.TAR_PATH)
                await self.download_chunk(url, size, 0, file)

                if not self.check_file_hash(self.TAR_PATH, hash):
                    self.remove_file(self.TAR_PATH)
                    log.info("Vfs update corrupt")
                    return False
                else:
                    log.info("Vfs update OK")
                    self.delete_old_vfs()
                    unpack = self.unpack_tar()
                    self.remove_file(self.TAR_PATH)
                    if not unpack:
                        return False

            else:
                self.copy_vfs()


        else:
            log.error("Update meta data corrupt")
            return False

        self.finish_update()



    # Partition Sector

    def check_signature(self, metadata):
        # you should implement a signature check.
        if self.next_boot_partition:
            return True
        else:
            return False

    async def request_file(self, url, f_id=0):
        r = "{}/{}".format(url, f_id)
        log.info('Chuck request url: {}'.format(r))

        while True:
            resp = await aiohttp.request("GET", r)
            break
        return resp


    async def download_chunk(self, url, update_size, f_id=0, file=None):

        resp = await self.request_file(url, f_id=f_id)

        if resp:
            log.info("board <-- from id: {}".format(f_id))

            pieces = int(update_size / self.CHUNK_SIZE) + (update_size % self.CHUNK_SIZE > 0)
            written_size = 0
            lst_piece = (pieces - 1)


            for i in range(0, pieces):

                while True:
                    try:
                        if i < lst_piece:
                            buf = await resp.content.readexactly(self.CHUNK_SIZE)
                        else:
                            buf = await resp.content.read(self.CHUNK_SIZE)

                    except Exception as e:
                        log.error("Download: {}".format(e))
                        buf = False
                        await resp.content.aclose()
                        break
                    break

                if buf:
                    if file:
                        written_size += self.write_file_chunk(buf, file)
                    else:
                        written_size += self.write_partition_chunk(buf, i)
                    log.info("<- {:.2%}".format(i / lst_piece))
                    if len(buf) < self.CHUNK_SIZE and i < lst_piece:
                        log.info("{} <- c_sz: {}, w_sz: {}".format(i, len(buf), written_size))
                        log.debug(buf)


            log.info("Pieces: {}".format(pieces))
            log.info("Update size: {}".format(update_size))
            log.info("Written size = {}".format(written_size))

            await resp.content.aclose()

            if written_size == 0:
                return False

            return True

        return False



    def copy_partition(self):
        buf = bytearray(self.CHUNK_SIZE)
        for i in range(0, self.partitions[self.cur_boot_partition][3]/self.CHUNK_SIZE):
            esp.flash_read(self.partitions[self.cur_boot_partition][2]+self.CHUNK_SIZE*i, buf)
            self.write_partition_chunk(buf, i)


    def delete_partition(self):
        buf = bytearray(self.CHUNK_SIZE)
        for i in range(0, self.partitions[self.next_boot_partition][3]/self.CHUNK_SIZE):
            self.write_partition_chunk(buf, i)


    def write_partition_chunk(self, buffer, id):
        chunkspersec = (self.SEC_SIZE//self.CHUNK_SIZE)

        if id%chunkspersec == 0:
            esp.flash_erase(self.next_boot_part_base_sec + id//chunkspersec)
        esp.flash_write(self.partitions[self.next_boot_partition][2]+self.CHUNK_SIZE*id, buffer)

        return len(buffer)

    def check_partition(self, hash, updatesize):
        h = hashlib.sha256()

        buf_sz = int((updatesize / self.CHUNK_SIZE - updatesize // self.CHUNK_SIZE) * self.CHUNK_SIZE)
        log.debug('First buf_sz {}'.format(buf_sz))
        if buf_sz == 0:
            buf = bytearray(self.CHUNK_SIZE)
        else:
            buf = bytearray(buf_sz)

        position = self.partitions[self.next_boot_partition][2]
        pieces = int(updatesize / self.CHUNK_SIZE) + (updatesize % self.CHUNK_SIZE > 0)

        for i in range(0, pieces):
            # log.debug('id {}, P:  {}'.format(i, position))
            esp.flash_read(position, buf)
            # log.debug('{}'.format(buf))

            h.update(buf)
            position += len(buf)
            buf = bytearray(self.CHUNK_SIZE)

        parthash = (ubinascii.hexlify(h.digest()).decode())

        log.info('partition hash is "{}", should be "{}"'.format(parthash, hash))
        return parthash == hash


    #VFS sector

    def remove_file(self, path):

        try:
            os.remove(path)
        except Exception as e:
            log.error("File not exist: {}".format(e))
            pass

    def write_file(self, path):

        self.remove_file(path)
        f = open(path, "ab")
        return f


    def write_file_chunk(self, buf, file):
        file.write(buf)
        file.flush()
        return len(buf)


    def check_file_hash(self, path, hash):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            buf = None
            while True:
                buf = f.read(self.CHUNK_SIZE)
                if not buf:
                    break
                h.update(buf)
        filehash = (ubinascii.hexlify(h.digest()).decode())
        log.info('{} hash is "{}", should be "{}"'.format(path, filehash, hash))
        return filehash == hash



    def delete_old_vfs(self):
        deep_delete_folder("/{}".format(self.next_boot_partition))
        os.mkdir("/{}".format(self.next_boot_partition))

    def copy_vfs(self):
        self.delete_old_vfs()
        deep_copy_folder("/{}".format(self.cur_boot_partition), "/{}".format(self.next_boot_partition))

    def unpack_tar(self):
        t = utar.TarFile(self.TAR_PATH)
        updatebasepath = "/{}/".format(self.next_boot_partition)
        log.info("Update Base Path: {}".format(updatebasepath))
        for i in t:
            # log.info("info {}".format(i))
            gc.collect()

            if i.type == utar.DIRTYPE:
                i_name = i.name[:-1]
                # log.debug("{} -> {}".format(i.name, i_name))
                try:
                    os.mkdir(updatebasepath + i_name)
                except Exception as e:
                    log.debug("mkdir: {}".format(e))
                    return False
            else:
                # log.info("file: {}".format(updatebasepath+i.name))
                with open(updatebasepath+i.name, 'wb') as ef:
                    pf = t.extractfile(i)
                    copy_file_obj(pf, ef)

        return True

    def finish_update(self):
        esp.ota_set_boot_partition(bytearray(self.partitions[self.next_boot_partition][6]))
        log.info("Update finished, restarting")
        machine.reset()