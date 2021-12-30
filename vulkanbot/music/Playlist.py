from collections import deque
import random
from config import config

from vulkanbot.music.Interfaces import IPlaylist
from vulkanbot.music.Song import Song



class Playlist(IPlaylist):
    """Class to manage and control the songs to play and played"""

    def __init__(self) -> None:
        self.__queue = deque()  # Store the musics to play
        self.__songs_history = deque()  # Store the musics played
        self.__name_history = deque()  # Store the name of musics played

        self.__looping_one = False
        self.__looping_all = False

        self.__current: Song = None

    @property
    def looping_one(self):
        return self.__looping_one

    @property
    def looping_all(self):
        return self.__looping_all

    @property
    def current(self):
        return self.__current

    @property
    def songs_to_preload(self) -> list:
        return list(self.__queue)[:config.MAX_PRELOAD_SONGS]

    def __len__(self):
            return len(self.__queue)

    def next_song(self) -> Song:
        """Return the next song to play"""
        if self.__current == None and len(self.__queue) == 0:   
            # If not playing and nothing to play
            return None

        # If playing
        played_song = self.__current

        # Check if need to repeat the played song
        if self.__looping_one:  # Insert the current song to play again
            self.__queue.appendleft(played_song)

        if self.__looping_all:  # Insert the current song in the end of queue
            self.__queue.append(played_song)

        while True:  # Try to get the source of next song
            if len(self.__queue) == 0:  # If no more song to play, return None
                return None

            self.__current = self.__queue[0]  # Att the current with the first one
            self.__queue.popleft()  # Remove the current from queue
            if self.__current.source == None: # Try until find one source
                continue
            
            else:
                self.__name_history.append(self.__current.title)  # Add to name history
                self.__songs_history.append(self.__current)  # Add to song history
                return self.__current

    def prev_song(self):
        """Return the source of the last song played

        Return None or the source of the prev song
        """
        if len(self.__songs_history) == 0:
            return None
        else:
            return self.__songs_history[0].source

    def add_song(self, identifier: str) -> Song:
        """Create a song object, add to queue and return it"""
        song = Song(identifier, self)  # Cria a musica com o identificador
        self.__queue.append(song)
        return song

    def shuffle(self) -> None:
        """Shuffle the order of the songs to play"""
        random.shuffle(self.__queue)

    def revert(self) -> None:
        """Revert the order of the songs to play"""
        self.__queue.reverse()

    def clear(self) -> None:
        """Clear the songs to play song history"""
        self.__queue.clear()
        self.__songs_history.clear()

    def loop_one(self) -> str:
        """Try to start the loop of the current song

        Return: Embed descrition to show to user
        """
        if self.__looping_all == True:
            return 'Vulkan already looping one music, disable loop first'
        elif self.__looping_one == True:
            return "I'm already doing this, you dumb ass"
        else:
            self.__looping_one = True
            return 'Repeating the current song'

    def loop_all(self) -> str:
        """Try to start the loop of all songs

        Return: Embed descrition to show to user
        """
        if self.__looping_one == True:
            return 'Vulkan already looping one music, disable loop first'
        elif self.__looping_all == True:
            return "I'm already doing this, you dumb ass"
        else:
            self.__looping_all = True
            return 'Repeating all songs in queue'

    def loop_off(self) -> str:
        """Disable both types of loop"""
        if self.__looping_all == False and self.__looping_one == False:
            return "The loop is already off, you fucking dick head"

        self.__looping_all = False
        self.__looping_one = False
        return 'Loop disable'

    def destroy_song(self, song_destroy: Song) -> None:
        """Destroy a song object from the queue"""
        for song in self.__queue:
            if song == song_destroy:
                self.__queue.remove(song)
                break
