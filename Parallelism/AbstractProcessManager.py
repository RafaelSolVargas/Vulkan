from abc import ABC, abstractmethod
from typing import Union
from discord.ext.commands import Context
from discord import Guild, Interaction
from Music.Song import Song
from Parallelism.ProcessInfo import PlayerInfo


class AbstractPlayersManager(ABC):
    def __init__(self, bot) -> None:
        pass

    @abstractmethod
    def setPlayerInfo(self, guild: Guild, info: PlayerInfo):
        pass

    @abstractmethod
    def getOrCreatePlayerInfo(self, guild: Guild, context: Union[Context, Interaction]) -> PlayerInfo:
        pass

    @abstractmethod
    def resetProcess(self, guild: Guild, context: Context) -> None:
        pass

    @abstractmethod
    def getRunningPlayerInfo(self, guild: Guild) -> PlayerInfo:
        pass

    @abstractmethod
    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        pass
