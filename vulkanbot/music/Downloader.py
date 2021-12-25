import re
from config import config
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError, DownloadError


class Downloader():
    """Download music source from Youtube with a music name or Youtube URL"""

    def __init__(self) -> None:
        self.__YDL_OPTIONS = {'format': 'bestaudio/best',
                              'default_search': 'auto',
                              'playliststart': 0,
                              'extract_flat': True,
                              'playlistend': config.MAX_PLAYLIST_LENGTH,
                              'cookiefile': config.COOKIE_PATH
                              }

    def download_one(self, music: str) -> list:
        """Download one music link from Youtube

        Arg: Music url or music name to search
        Return: List with the Youtube URL of the music
        """
        if type(music) != str:
            return

        if self.__is_url(music):  # If Url
            info = self.__download_url(music, flat=True)
        else:  # If Title
            info = self.__download_title(music)

        return info

    def download_many(self, music_list: list) -> list:
        """Download many music links from Youtube

        Arg: List with names or music url to search
        Return: List with the youtube URL of each music
        """
        if type(music_list) != list:
            return

        musics_info = []
        for music in music_list:
            info = self.download_one(music)
            musics_info.extend(info)

        return musics_info

    def download_full(self, link) -> dict:
        """Download the full music info with the video URL"""
        info = self.__download_url(url=link, flat=False)
        return info[0]

    def __download_title(self, music_name: str) -> list:
        """Download and return a list with the music link in dict"""
        with YoutubeDL(self.__YDL_OPTIONS) as ydl:
            try:
                result = ydl.extract_info(
                    f"ytsearch:{music_name}", download=False)
                id = result['entries'][0]['id']

                link = f"https://www.youtube.com/watch?v={id}"
                return [link]
            except Exception as e:
                raise e

    def __download_url(self, url: str, flat=True) -> list:
        """Download musics from Playlist URL or Music URL

        Arg: URL from Youtube
        Return: List of youtube links
        """
        options = self.__YDL_OPTIONS
        options['extract_flat'] = flat
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
