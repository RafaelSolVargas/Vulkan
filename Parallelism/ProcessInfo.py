from multiprocessing import Process, Queue, Lock
from Music.Playlist import Playlist


class ProcessInfo:
    """
    Class to store the reference to all structures to maintain a player process
    """

    def __init__(self, process: Process, queue: Queue, playlist: Playlist, lock: Lock) -> None:
        self.__process = process
        self.__queue = queue
        self.__playlist = playlist
        self.__lock = lock

    def setProcess(self, newProcess: Process) -> None:
        self.__process = newProcess

    def getProcess(self) -> Process:
        return self.__process

    def getQueue(self) -> Queue:
        return self.__queue

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> Lock:
        return self.__lock
