from multiprocessing import Queue, Lock
from multiprocessing.managers import BaseManager, NamespaceProxy
from typing import Dict
from Config.Singleton import Singleton
from discord import Guild
from discord.ext.commands import Context
from Parallelism.PlayerProcess import PlayerProcess
from Music.Playlist import Playlist
from Parallelism.ProcessInfo import ProcessInfo


class ProcessManager(Singleton):
    """
    Manage all running player process, creating and storing them for future calls
    Deal with the creation of shared memory
    """

    def __init__(self) -> None:
        if not super().created:
            VManager.register('Playlist', Playlist)
            self.__manager = VManager()
            self.__manager.start()
            self.__playersProcess: Dict[Guild, ProcessInfo] = {}

    def setPlayerContext(self, guild: Guild, context: ProcessInfo):
        self.__playersProcess[guild] = context

    def getPlayerContext(self, guild: Guild, context: Context) -> ProcessInfo:
        """Return the process info for the guild, if not, create one"""
        try:
            if guild not in self.__playersProcess.keys():
                self.__playersProcess[guild] = self.__createProcess(context)
            else:
                if not self.__playersProcess[guild].getProcess().is_alive():
                    self.__playersProcess[guild] = self.__createProcess(context)

            return self.__playersProcess[guild]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def getRunningPlayerInfo(self, guild: Guild) -> ProcessInfo:
        """Return the process info for the guild, if not, return None"""
        if guild not in self.__playersProcess.keys():
            return None

        return self.__playersProcess[guild]

    def __createProcess(self, context: Context):
        guildID: int = context.guild.id
        textID: int = context.channel.id
        voiceID: int = context.author.voice.channel.id
        authorID: int = context.author.id

        playlist: Playlist = self.__manager.Playlist()
        lock = Lock()
        queue = Queue()
        process = PlayerProcess(context.guild.name, playlist, lock, queue,
                                guildID, textID, voiceID, authorID)
        processInfo = ProcessInfo(process, queue, playlist, lock)

        return processInfo


class VManager(BaseManager):
    pass


class VProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
