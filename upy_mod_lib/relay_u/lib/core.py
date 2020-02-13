from db_u.tools import TbModel

class RelayControl:


    @classmethod
    def on(cls):
        cls.change_state(cls.on_value)


    @classmethod
    def off(cls):
        cls.change_state(1 - cls.on_value)


    @classmethod
    def get_state(cls):
        return cls._value()


    @classmethod
    def change_state(cls, _set=None):

        if _set is not None:
            cls._value(_set)
        else:
            cls._value(1 - cls._value())

        state = cls._value()
        if cls._cb:
            cls._cb(state)

        return state


class RelayModel(TbModel):

    def _func(self):

        self.relay_ctrl = RelayControl
        self.relay_ctrl.on_value = self.p_on
        self.relay_ctrl._cb = self.cb

    def cb(self, state):
        st = "OFF"
        if state == self.p_on:
            st = "ON"
        self.mbus.pub_h("relay/{}/state".format(self.name), st)

