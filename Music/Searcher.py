from Music.Types import Provider
from Music.Spotify import SpotifySearch
from Utils.Utils import is_url


class Searcher():
    def __init__(self) -> None:
        self.__Spotify = SpotifySearch()

    def search(self, music: str) -> list:
        provider = self.__identify_source(music)

        if provider == Provider.YouTube:
            return [music], Provider.YouTube

        elif provider == Provider.Spotify:
            if self.__Spotify.connected == True:
                musics = self.__Spotify.search(music)
                return musics, Provider.Name
            else:
                print('DEVELOPER NOTE -> Spotify Not Connected')
                return [], Provider.Unknown

        elif provider == Provider.Name:
            return [music], Provider.Name

        elif provider == Provider.Unknown:
            return None, Provider.Unknown

    def __identify_source(self, music) -> Provider:
        if not is_url(music):
            return Provider.Name

        if "https://www.youtu" in music or "https://youtu.be" in music or "https://music.youtube" in music:
            return Provider.YouTube

        if "https://open.spotify.com" in music:
            return Provider.Spotify

        return Provider.Unknown
