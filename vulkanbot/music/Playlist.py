from collections import deque
import random
from Song import Song


class Playlist():
    """Class to manage and control the songs to play and played"""

    def __init__(self) -> None:
        self.__queue = deque()  # Store the musics to play
        self.__songs_history = deque()  # Store the musics played
        self.__name_history = deque()  # Store the name of musics played

        self.__loop_one = False
        self.__loop_all = False

        self.__current = None

    def __len__(self):
        return len(self.queue)

    def next_song(self):
        """Return the source of the next song to play"""
        if self.__current == None:
            print('Nenhuma música tocando')
            return None

        if self.__loop_one:  # Insert the current song to play again
            self.__queue.appendleft(self.__current)

        if self.__loop_all:  # Insert the current song in the end of queue
            self.__queue.append(self.__current)

        if len(self.__queue) == 0:  # If nothing no more song to play, return
            return None

        played_song = self.__current
        # Add played song name to history
        self.__name_history.append(played_song.title)
        return self.__queue[0]  # Return the next song to play

    def prev_song(self):
        """Return the source of the last song played

        Return None or the source of the prev song
        """
        if len(self.__songs_history) == 0:
            return None
        else:
            return self.__songs_history[0].source

    def add_song(self, song: Song) -> None:
        """Receives a song object and store to the play queue"""
        if type(song) != Song:
            print('Song type invalid')
            return

        self.__queue.append(song)

    def shuffle(self):
        """Shuffle the order of the songs to play"""
        random.shuffle(self.__queue)

    def revert(self):
        """Revert the order of the songs to play"""
        self.__queue.reverse()

    def clear(self) -> None:
        """Clear the songs to play song history"""
        self.__queue.clear()
        self.__songs_history.clear()

    def play(self):
        """Start the play of the first musics and return his source"""
        if len(self.__queue) == 0:
            print('Nenhuma música para tocar')
            return None

        self.__current = self.__queue[0]
        return self.__queue[0].source

    def loop_one(self) -> str:
        """Try to start the loop of the current song

        Return: Embed descrition to show to user
        """
        if self.__loop_all == True:
            return 'Vulkan already looping one music, disable loop first'
        elif self.__loop_one == True:
            return "I'm already doing this, you dumb ass"
        else:
            self.__loop_one = True

    def loop_all(self) -> str:
        """Try to start the loop of all songs

        Return: Embed descrition to show to user
        """
        if self.__loop_one == True:
            return 'Vulkan already looping one music, disable loop first'
        elif self.__loop_all == True:
            return "I'm already doing this, you dumb ass"
        else:
            self.__loop_all = True

    def loop_off(self) -> None:
        """Disable both types of loop"""
        self.__loop_all = False
        self.__loop_one = False
