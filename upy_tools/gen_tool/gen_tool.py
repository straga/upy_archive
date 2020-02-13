# Copyright (c) 2018 Viktor Vorobjov

import subprocess
import os
import platform

print("Gent Tool")
# path_ulib = "../../lib/micropython-lib"
# work_path = "./example"
# work_lib_path = "./example/lib"

if platform.system() == 'Windows':
    symlink = "MKLINK"
else:
    symlink = "ln"
    

def create_symlink(symlink, p1, p2, arg=None):

    link = p1
    target = p2

    if symlink == "ln":
        link = p2
        target = p1

    cmd = [symlink, link, target]
    if arg:
        cmd = [symlink, arg, link, target]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.wait()
    print(process.stdout.read())


def create_lib(path, libs, path_ulib, file=False):

    if file:
        dir_dst = os.path.abspath("{}".format(path))
        if not os.path.exists(dir_dst):
            os.makedirs(dir_dst)

        arg = None
    else:
        arg = "/D"

    if symlink == "ln":
        arg = "-sf"




    for key, value in libs.items():
        target = os.path.abspath("{}/{}/{}".format(path_ulib, key, value))
        link = os.path.abspath("{}/{}".format(path, value))
        print("   ")
        print(link)
        # try:
        #     os.remove(link)
        # except Exception as e:
        #     print(e)
        #     pass
        if os.path.isfile(target):
            print("   ")
            print(link)
            create_symlink(symlink, link, target, arg)
        else:
            print("ERROR: Source not exist")
            print(link)


def gen_libs(libs):

    for lib in libs:
        _path = "{}/{}".format(lib["dst_lib"], lib["dst_path"])
        _lib = {lib["src_path"]: lib["src"]}
        _path_ulib = lib["src_lib"]
        _file = True
        if "file" in lib:
            _file = lib["file"]

        create_lib(path=_path, libs=_lib, path_ulib=_path_ulib, file=_file)