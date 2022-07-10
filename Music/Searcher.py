from Exceptions.Exceptions import InvalidInput, SpotifyError, YoutubeError
from Music.Downloader import Downloader
from Music.Types import Provider
from Music.Spotify import SpotifySearch
from Utils.Utils import Utils
from Utils.UrlAnalyzer import URLAnalyzer
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
            try:
                track = self.__cleanYoutubeInput(track)
                musics = await self.__down.extract_info(track)
                return musics
            except:
                raise YoutubeError(self.__messages.YOUTUBE_ERROR, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Spotify:
            try:
                musics = self.__Spotify.search(track)
                if musics == None or len(musics) == 0:
                    raise SpotifyError(self.__messages.SPOTIFY_ERROR, self.__messages.GENERIC_TITLE)

                return musics
            except SpotifyError as error:
                raise error  # Redirect already processed error
            except Exception as e:
                print(f'[Spotify Error] -> {e}')
                raise SpotifyError(self.__messages.SPOTIFY_ERROR, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Name:
            return [track]

    def __cleanYoutubeInput(self, track: str) -> str:
        trackAnalyzer = URLAnalyzer(track)
        # Just ID and List arguments probably
        if trackAnalyzer.queryParamsQuant <= 2:
            return track

        # Arguments used in Mix Youtube Playlists
        if 'start_radio' or 'index' in trackAnalyzer.queryParams.keys():
            return trackAnalyzer.getCleanedUrl()

    def __identify_source(self, track) -> Provider:
        if not Utils.is_url(track):
            return Provider.Name

        if "https://www.youtu" in track or "https://youtu.be" in track or "https://music.youtube" in track:
            return Provider.YouTube

        if "https://open.spotify.com" in track:
            return Provider.Spotify

        return Provider.Unknown
