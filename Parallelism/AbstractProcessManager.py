from abc import ABC, abstractmethod
from threading import Lock
from typing import Union
from discord.ext.commands import Context
from discord import Guild, Interaction
from Music.Playlist import Playlist
from Music.Song import Song
from Parallelism.Commands import VCommands


class AbstractPlayersManager(ABC):
    def __init__(self, bot) -> None:
        pass

    @abstractmethod
    async def sendCommandToPlayer(self, command: VCommands, guild: Guild, context: Union[Context, Interaction], forceCreation: bool = False):
        """If the forceCreation boolean is True, then the context must be provided for the Player to be created"""
        pass

    @abstractmethod
    def getPlayerPlaylist(self, guild: Guild) -> Playlist:
        """If there is a player process for the guild, then return the playlist of the guild"""
        pass

    @abstractmethod
    def getPlayerLock(self, guild: Guild) -> Lock:
        """If there is a player process for the guild, then return the lock of the guild"""
        pass

    @abstractmethod
    def verifyIfPlayerExists(self, guild: Guild) -> bool:
        """Returns if a player for the guild exists"""
        pass

    @abstractmethod
    def createPlayerForGuild(self, guild: Guild, context: Union[Context, Interaction]) -> None:
        """With the context information of a guild create a internal player for the guild"""
        pass

    @abstractmethod
    def resetPlayer(self, guild: Guild, context: Context) -> None:
        """Tries to reset the player of the guild"""
        pass

    @abstractmethod
    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        pass
