import re
from config import config
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError, DownloadError

from vulkanbot.music.Types import Provider


class Downloader():
    """Download musics direct URL and title or Source from Youtube using a music name or Youtube URL"""

    def __init__(self) -> None:
        self.__YDL_OPTIONS = {'format': 'bestaudio/best',
                              'default_search': 'auto',
                              'playliststart': 0,
                              'extract_flat': True,
                              'playlistend': config.MAX_PLAYLIST_LENGTH,
                              }

    def download_urls(self, musics_input, provider: Provider) -> list:
        """Download the musics direct URL from Youtube and return in a list 

        Arg: List with names or youtube url or a Unique String
        Return: List with the direct youtube URL of each music
        """
        if type(provider) != Provider:
            return None

        if type(musics_input) != list and type(musics_input) != str:
            return None

        if provider == Provider.Name:  # Send a list of names
            musics_urls = self.__download_titles(musics_input)
            return musics_urls

        elif provider == Provider.YouTube:  # Send a URL or Title
            url = self.__download_one(musics_input)
            return url
        else:
            return None

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
            except (ExtractorError, DownloadError) as e:  # Any type of error in download
                print(e)
                return None

    def __download_one(self, music: str) -> list:
        """Download one music/playlist direct link from Youtube

        Arg: Playlist URL or Music Name to download direct URL
        Return: List with the Youtube URL of each music downloaded
        """
        if type(music) != str:
            return

        if self.__is_url(music):  # If Url
            info = self.__download_links(music)  # List of dict
        else:  # If Title
            info = self.__download_titles(music)  # List of dict

        return info

    def __download_titles(self, musics_names: list) -> list:
        """Download a music direct URL using his name.

        Arg: Music Name
        Return: List with one dict, containing the music direct URL and title
        """
        if type(musics_names) == str:  # Turn str into list
            musics_names = [musics_names]

        musics_info = []
        with YoutubeDL(self.__YDL_OPTIONS) as ydl:
            try:
                for name in musics_names:
                    search = f"ytsearch:{name}"
                    result = ydl.extract_info(search, download=False)

                    id = result['entries'][0]['id']
                    music_info = {
                        'url': f"https://www.youtube.com/watch?v={id}",
                        'title': result['entries'][0]['title']
                    }
                    musics_info.append(music_info)

                return musics_info  # Return a list
            except Exception as e:
                raise e

    def __download_links(self, url: str) -> list:
        """Download musics direct links from Playlist URL or Music URL

        Arg_Url: URL from Youtube 
        Return: List of dicts, with the title and url of each music
        """
        options = self.__YDL_OPTIONS
        options['extract_flat'] = True
        with YoutubeDL(options) as ydl:
            try:
                result = ydl.extract_info(url, download=False)
                musics_info = []

                if result.get('entries'):  # If got a dict of musics
                    for entry in result['entries']:
                        music_info = {
                            'title': entry['title'],
                            'url': f"https://www.youtube.com/watch?v={entry['id']}"
                        }

                        musics_info.append(music_info)
                else:  # Or a single music
                    music_info = {
                        'url': result['original_url'],
                        'title': result['title']
                    }
                    musics_info.append(music_info)

                return musics_info  # Return a list
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



