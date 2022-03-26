from Exceptions.Exceptions import InvalidInput, SpotifyError
from Music.Downloader import Downloader
from Music.Types import Provider
from Music.Spotify import SpotifySearch
from Utils.Utils import Utils
from Config.Messages import SearchMessages


class Searcher():
    def __init__(self) -> None:
        self.__Spotify = SpotifySearch()
        self.__messages = SearchMessages()
        self.__down = Downloader()

    async def search(self, track: str) -> list:
        provider = self.__identify_source(track)
        if provider == Provider.Unknown:
            raise InvalidInput(self.__messages.UNKNOWN_INPUT, self.__messages.UNKNOWN_INPUT_TITLE)

        elif provider == Provider.YouTube:
            musics = await self.__down.extract_info(track)
            return musics

        elif provider == Provider.Spotify:
            try:
                musics = self.__Spotify.search(track)
                return musics
            except:
                raise SpotifyError(self.__messages.SPOTIFY_ERROR, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Name:
            return [track]

    def __identify_source(self, track) -> Provider:
        if not Utils.is_url(track):
            return Provider.Name

        if "https://www.youtu" in track or "https://youtu.be" in track or "https://music.youtube" in track:
            return Provider.YouTube

        if "https://open.spotify.com" in track:
            return Provider.Spotify

        return Provider.Unknown
