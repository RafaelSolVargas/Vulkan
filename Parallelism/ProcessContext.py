from multiprocessing import Process, Queue, Lock
from Music.Playlist import Playlist


class ProcessContext:
    def __init__(self, process: Process, queue: Queue, playlist: Playlist, lock: Lock) -> None:
        self.__process = process
        self.__queue = queue
        self.__playlist = playlist
        self.__lock = lock

    def getProcess(self) -> Process:
        return self.__process

    def getQueue(self) -> Queue:
        return self.__queue

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> Lock:
        return self.__lock
