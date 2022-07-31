from enum import Enum
from multiprocessing import Process, Queue, Lock
from discord import TextChannel
from Music.Playlist import Playlist


class ProcessStatus(Enum):
    RUNNING = 'Running'
    SLEEPING = 'Sleeping'


class ProcessInfo:
    """
    Class to store the reference to all structures to maintain a player process
    """

    def __init__(self, process: Process, queueToPlayer: Queue, queueToMain: Queue, playlist: Playlist, lock: Lock, textChannel: TextChannel) -> None:
        self.__process = process
        self.__queueToPlayer = queueToPlayer
        self.__queueToMain = queueToMain
        self.__playlist = playlist
        self.__lock = lock
        self.__textChannel = textChannel
        self.__status = ProcessStatus.RUNNING

    def setProcess(self, newProcess: Process) -> None:
        self.__process = newProcess

    def getStatus(self) -> ProcessStatus:
        return self.__status

    def setStatus(self, status: ProcessStatus) -> None:
        self.__status = status

    def getProcess(self) -> Process:
        return self.__process

    def getQueueToPlayer(self) -> Queue:
        return self.__queueToPlayer

    def getQueueToMain(self) -> Queue:
        return self.__queueToMain

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> Lock:
        return self.__lock

    def getTextChannel(self) -> TextChannel:
        return self.__textChannel
