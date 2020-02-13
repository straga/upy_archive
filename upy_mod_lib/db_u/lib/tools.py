

class TbModel:

    def __init__(self, *args, **kwargs):

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self._func()


    def _func(self):
        pass
