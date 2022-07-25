from multiprocessing import Queue, Lock
from multiprocessing.managers import BaseManager, NamespaceProxy
from typing import Dict
from Config.Singleton import Singleton
from discord import Guild
from discord.ext.commands import Context
from Parallelism.PlayerProcess import PlayerProcess
from Music.Playlist import Playlist
from Parallelism.ProcessInfo import ProcessInfo
from Parallelism.Commands import VCommands, VCommandsType


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
        self.__playersProcess[guild.id] = context

    def getPlayerInfo(self, guild: Guild, context: Context) -> ProcessInfo:
        """Return the process info for the guild, if not, create one"""
        try:
            if guild.id not in self.__playersProcess.keys():
                self.__playersProcess[guild.id] = self.__createProcessInfo(context)
            else:
                # If the process has ended create a new one
                if not self.__playersProcess[guild.id].getProcess().is_alive():
                    self.__playersProcess[guild.id] = self.__recreateProcess(context)

            return self.__playersProcess[guild.id]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def resetProcess(self, guild: Guild, context: Context) -> None:
        """Restart a running process, already start it to return to play"""
        if guild.id not in self.__playersProcess.keys():
            return None

        # Recreate the process keeping the playlist
        newProcessInfo = self.__recreateProcess(context)
        newProcessInfo.getProcess().start()  # Start the process
        # Send a command to start the play again
        playCommand = VCommands(VCommandsType.PLAY)
        newProcessInfo.getQueue().put(playCommand)
        self.__playersProcess[guild.id] = newProcessInfo

    def getRunningPlayerInfo(self, guild: Guild) -> ProcessInfo:
        """Return the process info for the guild, if not, return None"""
        if guild.id not in self.__playersProcess.keys():
            return None

        return self.__playersProcess[guild.id]

    def __createProcessInfo(self, context: Context) -> ProcessInfo:
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

    def __recreateProcess(self, context: Context) -> ProcessInfo:
        """Create a new process info using previous playlist"""
        guildID: int = context.guild.id
        textID: int = context.channel.id
        voiceID: int = context.author.voice.channel.id
        authorID: int = context.author.id

        playlist: Playlist = self.__playersProcess[guildID].getPlaylist()
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
