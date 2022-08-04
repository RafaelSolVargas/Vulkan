from enum import Enum


class MessagesCategory(Enum):
    QUEUE = 1
    HISTORY = 2
    LOOP = 3
    NOW_PLAYING = 4
    PLAYER = 5
    MANAGING_QUEUE = 6
    OTHERS = 7
