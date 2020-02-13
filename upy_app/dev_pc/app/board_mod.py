
import logging

from board.cfg_db import mod_debug
mod_debug()

#board
log = logging.getLogger("BOARD")
log.setLevel(logging.INFO)

from board.cfg_db import _name_board
import sys



class uCore:
    def __init__(self, mbus, umod, board):
        self.mbus = mbus
        self.umod = umod
        self.board = board


class Activate:

    def __init__(self, mbus, umod, board_id):

        self.mbus = mbus
        self.umod = umod

        log.info("BID: {}".format(board_id))

        s_mod = umod.mod_sel("board_cfg")

        if not len(s_mod):
            from mod_u.model import init_db
            init_db(umod)
            del sys.modules["mod_u.model"]

        from board.cfg_db import push_board
        push_board(umod)


        board = _name_board

        _modules = umod.call_cmd("_scan", "board_mod")

        for mod in _modules:
            if mod["active"]:
                name_mod = mod["name"]
                try:
                    init_db = __import__("{}_mod".format(name_mod)).init_db
                    init_db(umod)
                    log.info("MOD DB ACTIVATE: {}".format(name_mod))
                    del sys.modules["{}_mod".format(name_mod)]

                except Exception as e:
                    log.info("MOD: {}, init db err: {}".format(mod, e))


        from board.cfg_db import push_data
        push_data(umod)
        del sys.modules["board.cfg_db"]

        umod.call_cmd("_upd", "board_cfg", {"board": _name_board}, init=1, uid=board_id.decode())


        # s_mod = umod.rec_sel("cfg_board", name=_name_board)
        # if len(s_mod):
        #     board = s_mod[0]["board"]
        #     if s_mod[0]["init"] == 0:
        #         from board.cfg_db import push_data
        #         push_data(umod)
        #         umod.rec_upd("cfg_board", {"board": board}, init=1, uid=board_id.decode())
        # else:
        #     log.info("BOARD: NOT CONFIGURE")


        self.core = uCore(mbus, umod, board)
        for mod in _modules:
            if mod["active"]:
                name_mod = mod["name"]

                try:
                    init_act = __import__("{}_mod".format(name_mod)).init_act
                    self.core = init_act(self.core)
                    log.info("MOD ACT ACTIVATE: {}".format(name_mod))
                    del sys.modules["{}_mod".format(name_mod)]
                    # umod.call_cmd("_upd", "board_mod", {"name": name_mod}, status="loaded")
                except Exception as e:
                    log.info("MOD: {}, activate err: {}".format(mod, e))










