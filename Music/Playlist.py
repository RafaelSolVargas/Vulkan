from collections import deque
from typing import List
from Config.Config import Configs
from Music.Interfaces import IPlaylist
from Music.Song import Song
import random


class Playlist(IPlaylist):

    def __init__(self) -> None:
        self.__config = Configs()
        self.__queue = deque()  # Store the musics to play
        self.__songs_history = deque()  # Store the musics played

        self.__looping_one = False
        self.__looping_all = False

        self.__current: Song = None

    @property
    def songs_history(self) -> deque:
        return self.__songs_history

    @property
    def looping_one(self) -> bool:
        return self.__looping_one

    @property
    def looping_all(self) -> bool:
        return self.__looping_all

    @property
    def current(self) -> Song:
        return self.__current

    @property
    def songs_to_preload(self) -> List[Song]:
        return list(self.__queue)[:self.__config.MAX_PRELOAD_SONGS]

    def __len__(self) -> int:
        return len(self.__queue)

    def next_song(self) -> Song:
        if self.__current == None and len(self.__queue) == 0:
            return None

        played_song = self.__current

        # Att played song info
        if played_song != None:
            if not self.__looping_one and not self.__looping_all:
                if played_song.problematic == False:
                    self.__songs_history.appendleft(played_song)

                if len(self.__songs_history) > self.__config.MAX_SONGS_HISTORY:
                    self.__songs_history.pop()  # Remove the older

            elif self.__looping_one:  # Insert the current song to play again
                self.__queue.appendleft(played_song)

            elif self.__looping_all:  # Insert the current song in the end of queue
                self.__queue.append(played_song)

        # Get the new song
        if len(self.__queue) == 0:
            return None

        self.__current = self.__queue.popleft()
        return self.__current

    def prev_song(self) -> Song:
        if len(self.__songs_history) == 0:
            return None
        else:
            if self.__current != None:
                self.__queue.appendleft(self.__current)

            last_song = self.__songs_history.popleft()  # Get the last song
            self.__current = last_song
            return self.__current  # return the song

    def add_song(self, identifier: str, requester: str) -> Song:
        song = Song(identifier=identifier, playlist=self, requester=requester)
        self.__queue.append(song)
        return song

    def shuffle(self) -> None:
        random.shuffle(self.__queue)

    def revert(self) -> None:
        self.__queue.reverse()

    def clear(self) -> None:
        self.__queue.clear()

    def loop_one(self) -> None:
        self.__looping_one = True
        self.__looping_all = False

    def loop_all(self) -> None:
        self.__looping_all = True
        self.__looping_one = False

    def loop_off(self) -> str:
        self.__looping_all = False
        self.__looping_one = False

    def destroy_song(self, song_destroy: Song) -> None:
        for song in self.__queue:
            if song == song_destroy:
                self.__queue.remove(song)
                break

    def move_songs(self, pos1, pos2) -> str:
        if pos1 == -1:
            pos1 = len(self.__queue)
        if pos2 == -1:
            pos2 = len(self.__queue)

        if pos2 not in range(1, len(self.__queue) + 1) or pos1 not in range(1, len(self.__queue) + 1):
            return self.__config.LENGTH_ERROR

        try:
            song = self.__queue[pos1-1]
            self.__queue.remove(song)
            self.__queue.insert(pos2-1, song)

            song1_name = song.title if song.title else song.identifier

            return self.__config.SONG_MOVED_SUCCESSFULLY.format(song1_name, pos1, pos2)
        except:
            return self.__config.ERROR_MOVING

    def remove_song(self, position) -> str:
        if position == -1:
            position = len(self.__queue)

        if position not in range(1, len(self.__queue) + 1):
            return self.__config.LENGTH_ERROR
        else:
            song = self.__queue[position-1]
            self.__queue.remove(song)

            song_name = song.title if song.title else song.identifier

            return self.__config.SONG_REMOVED_SUCCESSFULLY.format(song_name)

    def history(self) -> list:
        titles = []
        for song in self.__songs_history:
            title = song.title if song.title else 'Unknown'
            titles.append(title)

        return titles
