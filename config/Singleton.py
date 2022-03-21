class Singleton(object):
    __instance = None
    __created = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @property
    def created(cls):
        if cls.__created == False:
            cls.__created = True
            return False
        else:
            return True
