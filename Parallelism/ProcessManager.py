from multiprocessing import Queue, Lock
from multiprocessing.managers import BaseManager, NamespaceProxy
from typing import Dict
from Config.Singleton import Singleton
from discord import Guild, Client
from discord.ext.commands import Context
from Parallelism.PlayerProcess import PlayerProcess
from Music.Playlist import Playlist
from Parallelism.ProcessContext import ProcessContext


class ProcessManager(Singleton):
    def __init__(self, bot: Client = None) -> None:
        if not super().created:
            Manager.register('Playlist', Playlist)
            self.__manager = Manager()
            self.__manager.start()
            if bot is not None:
                self.__bot: Client = bot
                self.__playersProcess: Dict[Guild, ProcessContext] = {}

    def setPlayerContext(self, guild: Guild, context: ProcessContext):
        self.__playersProcess[guild] = context

    def getPlayerContext(self, guild: Guild, context: Context) -> ProcessContext:
        try:
            if guild not in self.__playersProcess.keys():
                self.__playersProcess[guild] = self.__createProcess(context)
            else:
                if not self.__playersProcess[guild].getProcess().is_alive():
                    self.__playersProcess[guild] = self.__createProcess(context)

            return self.__playersProcess[guild]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def getRunningPlayerContext(self, guild: Guild) -> ProcessContext:
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
        process = PlayerProcess(playlist, lock, queue, guildID, textID, voiceID, authorID)
        processContext = ProcessContext(process, queue, playlist, lock)
        return processContext


class Manager(BaseManager):
    pass


class ProxyBase(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
