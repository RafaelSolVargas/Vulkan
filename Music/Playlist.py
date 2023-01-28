from collections import deque
from typing import List
from Config.Configs import VConfigs
from Music.Song import Song
import random


class Playlist:

    def __init__(self) -> None:
        self.__configs = VConfigs()
        self.__queue = deque()  # Store the musics to play
        self.__songs_history = deque()  # Store the musics played

        self.__looping_one = False
        self.__looping_all = False

        self.__current: Song = None

    def getSongs(self) -> deque[Song]:
        return self.__queue

    def validate_position(self, position: int) -> bool:
        if position not in range(1, len(self.__queue) + 1):
            return False
        else:
            return True

    def validate_positions_list(self, positions: list) -> bool:
        for position in positions:
            if not self.validate_position(position):
                return False
        return True

    def getSongsHistory(self) -> deque:
        return self.__songs_history

    def isLoopingOne(self) -> bool:
        return self.__looping_one

    def isLoopingAll(self) -> bool:
        return self.__looping_all

    def getCurrentSong(self) -> Song:
        return self.__current

    def setCurrentSong(self, song: Song) -> Song:
        self.__current = song

    def getSongsToPreload(self) -> List[Song]:
        return list(self.__queue)[:self.__configs.MAX_PRELOAD_SONGS]

    def getSongsPages(self) -> List[List[Song]]:
        songsPages = []
        for x in range(0, len(self.__queue), self.__configs.MAX_SONGS_IN_PAGE):
            endIndex = x + self.__configs.MAX_SONGS_IN_PAGE
            startIndex = x
            songsPages.append(list(self.__queue)[startIndex:endIndex])

        return songsPages

    def __len__(self) -> int:
        return len(self.__queue)

    def next_song(self) -> Song:
        if self.__current is None and len(self.__queue) == 0:
            return None

        played_song = self.__current

        # Att played song info
        if played_song != None:
            if not self.__looping_one and not self.__looping_all:
                if not played_song.problematic:
                    self.__songs_history.appendleft(played_song)

                if len(self.__songs_history) > self.__configs.MAX_SONGS_HISTORY:
                    self.__songs_history.pop()  # Remove the older

            elif self.__looping_one:  # Insert the current song to play again
                self.__queue.appendleft(played_song)

            elif self.__looping_all:  # Insert the current song in the end of queue
                self.__queue.append(played_song)

        # Get the new song
        if len(self.__queue) == 0:
            self.__current = None
            return None

        self.__current: Song = self.__queue.popleft()
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

    def add_song(self, song: Song) -> Song:
        self.__queue.append(song)
        return song

    def add_song_start(self, song: Song) -> Song:
        self.__queue.insert(0, song)
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
        song = self.__queue[pos1-1]
        self.__queue.remove(song)
        self.__queue.insert(pos2-1, song)

        return song

    def remove_song(self, position) -> str:
        song = self.__queue[position-1]
        self.__queue.remove(song)

        return song

    def getHistory(self) -> list:
        titles = []
        for song in self.__songs_history:
            title = song.title if song.title else 'Unknown'
            titles.append(title)

        return titles
