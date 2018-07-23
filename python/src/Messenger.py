class Messenger(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def getDict(self):
        return self.__dict__
