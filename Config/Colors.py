from Config.Singleton import Singleton


class VColors(Singleton):
    def __init__(self) -> None:
        self.__red = 0xDC143C
        self.__green = 0x1F8B4C
        self.__grey = 0x708090
        self.__blue = 0x206694
        self.__black = 0x23272A

    @property
    def RED(self) -> str:
        return self.__red

    @property
    def GREEN(self) -> str:
        return self.__green

    @property
    def GREY(self) -> str:
        return self.__grey

    @property
    def BLUE(self) -> str:
        return self.__blue

    @property
    def BLACK(self) -> str:
        return self.__black

    @property
    def RED(self) -> str:
        return self.__red
