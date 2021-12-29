from collections import deque
import random
from vulkanbot.music.Song import Song
from vulkanbot.music.Downloader import Downloader


class Playlist():
    """Class to manage and control the songs to play and played"""

    def __init__(self) -> None:
        self.__down = Downloader()
        self.__queue = deque()  # Store the musics to play
        self.__songs_history = deque()  # Store the musics played
        self.__name_history = deque()  # Store the name of musics played

        self.__looping_one = False
        self.__looping_all = False

        self.__current = None

    @property
    def looping_one(self):
        return self.__looping_one

    @property
    def looping_all(self):
        return self.__looping_all

    def __len__(self):
        if self.__looping_one == True or self.__looping_all == True:
            return 1
        else:
            return len(self.__queue)

    def next_song(self):
        """Return the source of the next song to play"""
        if self.__current == None:  # If not playing
            if len(self.__queue) == 0:  # If nothing to play
                return None
            else:  # If there is music to play
                return self.__start()

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

            # If there is more to play
            # Finish download of the next song
            source = self.__prepare_next(self.__queue[0])
            if source == None:  # If there is a problem in the download
                self.__queue.popleft()  # Remove the music with problems
                continue

            return source

    def get_current(self):
        """Return current music embed"""
        if self.__current:
            return self.__current.embed()
        else:
            return 'Nenhuma música tocando'

    def __prepare_next(self, next_song: Song) -> str:
        """Finish the download of the music and return the source"""
        if next_song.source == None:  # Check if source has already downloaded
            url = next_song.url  # Get the URL
            info = self.__down.download_source(url)  # Download the source
            if info == None:  # If there is a problem in the download
                return None

            next_song.finish_down(info)  # Updating the info of song

        # Att the Playlist info
        self.__current = next_song  # Att the current
        self.__queue.popleft()  # Remove the current from queue
        self.__name_history.append(self.__current.title)  # Add to name history
        self.__songs_history.append(self.__current)  # Add to song history

        return self.__current.source  # Return the source of current

    def __start(self) -> None:
        """Start the play of the first musics and return his source"""
        # Finish download of the next song
        url = self.__queue[0].url  # Get the URL
        info = self.__down.download_source(url)  # Download the source

        self.__queue[0].finish_down(info)  # Att the song

        # Att Playlist info
        self.__current = self.__queue[0]  # Att the current
        self.__queue.popleft()  # Remove the current from queue
        self.__name_history.append(self.__current.title)  # Add to name history
        self.__songs_history.append(self.__current)  # Add to song history

        return self.__current.source  # Return the source of current

    def prev_song(self):
        """Return the source of the last song played

        Return None or the source of the prev song
        """
        if len(self.__songs_history) == 0:
            return None
        else:
            return self.__songs_history[0].source

    def add_song(self, music: dict) -> None:
        """Receives a music object and store to the play queue"""
        if (not 'title' in music.keys()) or (not 'url' in music.keys()):
            print('Music without necessary keys')
            return

        song = Song(title=music['title'], url=music['url'])  # Cria a musica
        self.__queue.append(song)

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

    def queue(self) -> list:
        list_songs = []
        for song in self.__queue:
            title = song.title
            list_songs.append(title)
        return list_songs
