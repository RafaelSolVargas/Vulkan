import asyncio
import concurrent.futures

from config import config
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError, DownloadError

from vulkanbot.music.Song import Song
from vulkanbot.music.utils import is_url


class Downloader():
    """Download musics direct URL and title or Source from Youtube using a music name or Youtube URL"""

    def __init__(self) -> None:
        self.__YDL_OPTIONS = {'format': 'bestaudio/best',
                              'default_search': 'auto',
                              'playliststart': 0,
                              'extract_flat': True,
                              'playlistend': config.MAX_PLAYLIST_LENGTH,
                              }

    def download_one(self, song: Song) -> Song:
        """Receives a song object, finish his download and return it"""
        if song.identifier == None:
            return None

        if is_url(song.identifier):  # Youtube URL
            song_info = self.__download_url(song.identifier)
        else:  # Song name
            song_info = self.__download_title(song.identifier)

        if song_info == None:
            song.destroy()  # Destroy the music with problems
            return None
        else:
            song.finish_down(song_info)
            return song

    def extract_youtube_link(self, playlist_url: str) -> list:
        """Extract all songs direct URL from a Youtube Link

        Arg: Url String
        Return: List with the direct youtube URL of each song
        """
        if is_url(playlist_url):  # If Url
            options = self.__YDL_OPTIONS
            options['extract_flat'] = True

            with YoutubeDL(options) as ydl:
                try:
                    result = ydl.extract_info(playlist_url, download=False)
                    songs_identifiers = []

                    if result.get('entries'):  # If got a dict of musics
                        for entry in result['entries']:
                            songs_identifiers.append(
                                f"https://www.youtube.com/watch?v={entry['id']}")

                    else:  # Or a single music
                        songs_identifiers.append(result['original_url'])

                    return songs_identifiers  # Return a list
                except (ExtractorError, DownloadError) as e:
                    return None
        else:
            print('Invalid type of playlist URL')
            return None

    async def preload(self, songs: list) -> None:
        """Download the full info of the song object"""
        for song in songs:
            asyncio.ensure_future(self.__download_songs(song))

    def __download_url(self, url) -> dict:
        """Download musics full info and source from Music URL

        Arg: URL from Youtube 
        Return: Dict with the full youtube information of the music, including source to play it
        """
        options = self.__YDL_OPTIONS
        options['extract_flat'] = False

        with YoutubeDL(options) as ydl:
            try:
                result = ydl.extract_info(url, download=False)

                return result
            except (ExtractorError, DownloadError) as e:  # Any type of error in download
                return None

    async def __download_songs(self, song: Song) -> None:
        """Download a music object asynchronously"""
        if song.source != None:  # If Music already preloaded
            return

        def download_song(song):
            if is_url(song.identifier):  # Youtube URL
                song_info = self.__download_url(song.identifier)
            else:  # Song name
                song_info = self.__download_title(song.identifier)

            if song_info == None:
                song.destroy()  # Remove the song with problems from the playlist
            else:
                song.finish_down(song_info)

        # Creating a loop task to download each song
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=config.MAX_PRELOAD_SONGS
        )
        await asyncio.wait(fs={loop.run_in_executor(executor, download_song, song)},
                           return_when=asyncio.ALL_COMPLETED)

    def __download_title(self, title: str) -> dict:
        """Download a music full information using his name.

        Arg: Music Name
        Return: A dict containing the song information
        """
        if type(title) != str:
            return None

        config = self.__YDL_OPTIONS
        config['extract_flat'] = False

        with YoutubeDL(self.__YDL_OPTIONS) as ydl:
            try:
                search = f"ytsearch:{title}"
                result = ydl.extract_info(search, download=False)

                if result == None:
                    return None

                # Return a dict with the full info of first music
                return result['entries'][0]
            except Exception as e:
                return None
