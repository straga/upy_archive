

class Pin:

    OUT = 4
    IN = 5
    PULL_UP = 6
    PULL_DOWN = 6


    def __init__(self, id=None, mode=None, pull=None, value=None):

        self.id = "g_pin_{}".format(id)
        self.mode = mode
        self.pull = pull

        if value:
            self.value(value)


    def value(self, val=None):

        if val is None:
            return 0
        else:
            return 1


