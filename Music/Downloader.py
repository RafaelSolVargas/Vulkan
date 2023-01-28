import asyncio
from typing import List
from Config.Configs import VConfigs
from yt_dlp import YoutubeDL, DownloadError
from concurrent.futures import ThreadPoolExecutor
from Music.Song import Song
from Utils.Utils import Utils, run_async
from Config.Exceptions import DownloadingError


class Downloader:
    config = VConfigs()
    __YDL_OPTIONS = {'format': 'bestaudio/best',
                     'default_search': 'auto',
                     'playliststart': 0,
                     'extract_flat': False,
                     'playlistend': config.MAX_PLAYLIST_LENGTH,
                     'quiet': True,
                     'ignore_no_formats_error': True
                     }
    __YDL_OPTIONS_EXTRACT = {'format': 'bestaudio/best',
                             'default_search': 'auto',
                             'playliststart': 0,
                             'extract_flat': True,
                             'playlistend': config.MAX_PLAYLIST_LENGTH,
                             'quiet': True,
                             'ignore_no_formats_error': True
                             }
    __YDL_OPTIONS_FORCE_EXTRACT = {'format': 'bestaudio/best',
                                   'default_search': 'auto',
                                   'playliststart': 0,
                                   'extract_flat': False,
                                   'playlistend': config.MAX_PLAYLIST_LENGTH,
                                   'quiet': True,
                                   'ignore_no_formats_error': True
                                   }
    __BASE_URL = 'https://www.youtube.com/watch?v={}'

    def __init__(self) -> None:
        self.__config = VConfigs()
        self.__music_keys_only = ['resolution', 'fps', 'quality']
        self.__not_extracted_keys_only = ['ie_key']
        self.__not_extracted_not_keys = ['entries']
        self.__playlist_keys = ['entries']

    def finish_one_song(self, song: Song) -> Song:
        try:
            if song.identifier is None:
                return None

            if Utils.is_url(song.identifier):
                song_info = self.__download_url(song.identifier)
            else:
                song_info = self.__download_title(song.identifier)

            song.finish_down(song_info)
            return song
        # Convert yt_dlp error to my own error
        except DownloadError as e:
            raise DownloadingError(e.msg)

    @run_async
    def extract_info(self, url: str) -> List[dict]:
        if url == '':
            return []

        if Utils.is_url(url):  # If Url
            options = Downloader.__YDL_OPTIONS_EXTRACT
            with YoutubeDL(options) as ydl:
                try:
                    extracted_info = ydl.extract_info(url, download=False)
                    # Some links doesn't extract unless extract_flat key is passed as False in options
                    if self.__failed_to_extract(extracted_info):
                        extracted_info = self.__get_forced_extracted_info(url)

                    if self.__is_music(extracted_info):
                        return [extracted_info['original_url']]

                    elif self.__is_multiple_musics(extracted_info):
                        songs = []
                        for song in extracted_info['entries']:
                            songs.append(self.__BASE_URL.format(song['id']))
                        return songs

                    else:  # Failed to extract the songs
                        print(f'DEVELOPER NOTE -> Failed to Extract URL {url}')
                        return []
                # Convert the yt_dlp download error to own error
                except DownloadError:
                    raise DownloadingError()
                except Exception as e:
                    print(f'DEVELOPER NOTE -> Error Extracting Music: {e}, {type(e)}')
                    raise e
        else:
            return []

    def __get_forced_extracted_info(self, url: str) -> list:
        options = Downloader.__YDL_OPTIONS_FORCE_EXTRACT
        with YoutubeDL(options) as ydl:
            try:
                extracted_info = ydl.extract_info(url, download=False)
                return extracted_info

            except Exception as e:
                print(f'DEVELOPER NOTE -> Error Forcing Extract Music: {e}')
                return []

    def __download_url(self, url) -> dict:
        options = Downloader.__YDL_OPTIONS
        with YoutubeDL(options) as ydl:
            try:
                result = ydl.extract_info(url, download=False)

                return result
            except Exception as e:  # Any type of error in download
                print(f'DEVELOPER NOTE -> Error Downloading {url} -> {e}')
                return None

    async def download_song(self, song: Song) -> None:
        if song.source is not None:  # If Music already preloaded
            return None

        def __download_func(song: Song) -> None:
            try:
                if Utils.is_url(song.identifier):
                    song_info = self.__download_url(song.identifier)
                else:
                    song_info = self.__download_title(song.identifier)

                song.finish_down(song_info)
            except Exception as e:
                print(f'DEVELOPER NOTE -> Error Downloading {song.identifier} -> {e}')

        # Creating a loop task to download each song
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=self.__config.MAX_PRELOAD_SONGS)
        fs = {loop.run_in_executor(executor, __download_func, song)}
        await asyncio.wait(fs=fs, return_when=asyncio.ALL_COMPLETED)

    def __download_title(self, title: str) -> dict:
        options = Downloader.__YDL_OPTIONS
        with YoutubeDL(options) as ydl:
            try:
                search = f'ytsearch:{title}'
                extracted_info = ydl.extract_info(search, download=False)

                if self.__failed_to_extract(extracted_info):
                    extracted_info = self.__get_forced_extracted_info(title)

                if extracted_info is None:
                    return {}

                if self.__is_multiple_musics(extracted_info):
                    if len(extracted_info['entries']) == 0:
                        return {}
                    return extracted_info['entries'][0]
                else:
                    print(f'DEVELOPER NOTE -> Failed to extract title {title}')
                    return {}
            except Exception as e:
                print(f'DEVELOPER NOTE -> Error downloading title {title}: {e}')
                return {}

    def __is_music(self, extracted_info: dict) -> bool:
        for key in self.__music_keys_only:
            if key not in extracted_info.keys():
                return False
        return True

    def __is_multiple_musics(self, extracted_info: dict) -> bool:
        for key in self.__playlist_keys:
            if key not in extracted_info.keys():
                return False
        return True

    def __failed_to_extract(self, extracted_info: dict) -> bool:
        if type(extracted_info) is not dict:
            return False

        for key in self.__not_extracted_keys_only:
            if key not in extracted_info.keys():
                return False
        for key in self.__not_extracted_not_keys:
            if key in extracted_info.keys():
                return False
        return True
