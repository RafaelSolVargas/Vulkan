from enum import Enum
from typing import Tuple


class VCommandsType(Enum):
    PREV = 'Prev'
    SKIP = 'Skip'
    PAUSE = 'Pause'
    RESUME = 'Resume'
    CONTEXT = 'Context'
    PLAY = 'Play'
    STOP = 'Stop'
    RESET = 'Reset'


class VCommands:
    def __init__(self, type: VCommandsType, args=None) -> None:
        self.__type = type
        self.__args = args

    def getType(self) -> VCommandsType:
        return self.__type

    def getArgs(self) -> Tuple:
        return self.__args
