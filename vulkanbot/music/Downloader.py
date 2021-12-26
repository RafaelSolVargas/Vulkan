import re
from config import config
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError, DownloadError


class Downloader():
    """Download musics direct URL or Source from Youtube using a music name or Youtube URL"""

    def __init__(self) -> None:
        self.__YDL_OPTIONS = {'format': 'bestaudio/best',
                              'default_search': 'auto',
                              'playliststart': 0,
                              'extract_flat': True,
                              'playlistend': config.MAX_PLAYLIST_LENGTH,
                              }

    def download_urls(self, musics_input) -> list:
        """Download the musics direct URL from Youtube and return in a list 

        Arg: List with names or youtube url or a Unique String
        Return: List with the direct youtube URL of each music
        """
        if type(musics_input) != list and type(musics_input) != str:
            return

        if type(musics_input) == str:  # Turn the string in a list
            musics_input = [musics_input]

        musics_urls = []
        for music in musics_input:
            url = self.__download_one(music)
            musics_urls.extend(url)

        return musics_urls

    def download_source(self, url) -> dict:
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
            except ExtractorError or DownloadError:
                pass

    def __download_one(self, music: str) -> list:
        """Download one music/playlist direct link from Youtube

        Arg: Playlist URL or Music Name to download direct URL
        Return: List with the Youtube URL of each music downloaded
        """
        if type(music) != str:
            return

        if self.__is_url(music):  # If Url
            info = self.__download_links(music)
        else:  # If Title
            info = self.__download_title(music)

        return info

    def __download_title(self, music_name: str) -> list:
        """Download a music direct URL using his name.

        Arg: Music Name
        Return: List with one item, the music direct URL
        """
        with YoutubeDL(self.__YDL_OPTIONS) as ydl:
            try:
                search = f"ytsearch:{music_name}"
                result = ydl.extract_info(search, download=False)
                id = result['entries'][0]['id']

                link = f"https://www.youtube.com/watch?v={id}"
                return [link]
            except Exception as e:
                raise e

    def __download_links(self, url: str) -> list:
        """Download musics direct links from Playlist URL or Music URL

        Arg_Url: URL from Youtube 
        Return: List of youtube information of each music
        """
        options = self.__YDL_OPTIONS
        options['extract_flat'] = True
        with YoutubeDL(options) as ydl:
            try:
                result = ydl.extract_info(url, download=False)

                musics_link = []

                if result.get('entries'):  # If got a dict of musics
                    for entry in result['entries']:
                        link = f"https://www.youtube.com/watch?v={entry['id']}"
                        musics_link.append(link)
                else:  # Or a single music
                    musics_link.append(result['original_url'])

                return musics_link
            except ExtractorError or DownloadError:
                pass

    def __is_url(self, string) -> bool:
        """Verify if a string is a url"""
        regex = re.compile(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        if re.search(regex, string):
            return True
        else:
            return False
