from db_u.tools import TbModel


try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio
    pass



class PushModel(TbModel):

    def _func(self):

        loop = asyncio.get_event_loop()
        loop.create_task(self.push_check())

    def change_state(self,):

        state = self._value()
        if self.cb:
            self.cb(state)

        return state

    def cb(self, state):

        _state = "OFF"
        if self.p_on == state:
            _state = "ON"

        self.mbus.pub_h("push/{}/state".format(self.name), _state)


    async def push_check(self):

        while True:
            if self._value() != self.value:
                self.value = self.change_state()
            await asyncio.sleep(0.3)


