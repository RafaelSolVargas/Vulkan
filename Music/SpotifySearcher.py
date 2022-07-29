from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from Config.Exceptions import SpotifyError
from Config.Configs import VConfigs
from Config.Messages import SpotifyMessages


class SpotifySearch():
    def __init__(self) -> None:
        self.__messages = SpotifyMessages()
        self.__config = VConfigs()
        self.__connected = False
        self.__connect()

    def __connect(self) -> None:
        try:
            auth = SpotifyClientCredentials(self.__config.SPOTIFY_ID, self.__config.SPOTIFY_SECRET)
            self.__api = Spotify(auth_manager=auth)
            self.__connected = True
        except Exception as e:
            print(f'DEVELOPER NOTE -> Spotify Connection Error {e}')

    def search(self, url: str) -> list:
        if not self.__checkUrlValid(url):
            raise SpotifyError(self.__messages.INVALID_SPOTIFY_URL, self.__messages.GENERIC_TITLE)

        type = url.split('/')[3].split('?')[0]
        code = url.split('/')[4].split('?')[0]
        musics = []

        try:
            if self.__connected:
                if type == 'album':
                    musics = self.__get_album(code)
                elif type == 'playlist':
                    musics = self.__get_playlist(code)
                elif type == 'track':
                    musics = self.__get_track(code)
                elif type == 'artist':
                    musics = self.__get_artist(code)

            return musics
        except SpotifyException:
            raise SpotifyError(self.__messages.INVALID_SPOTIFY_URL, self.__messages.GENERIC_TITLE)

    def __get_album(self, code: str) -> list:
        results = self.__api.album_tracks(code)
        musics = results['items']

        while results['next']:  # Get the next pages
            results = self.__api.next(results)
            musics.extend(results['items'])

        musicsTitle = []

        for music in musics:
            title = self.__extract_title(music)
            musicsTitle.append(title)

        return musicsTitle

    def __get_playlist(self, code: str) -> list:
        results = self.__api.playlist_items(code)
        itens = results['items']

        while results['next']:  # Load the next pages
            results = self.__api.next(results)
            itens.extend(results['items'])

        musics = []
        for item in itens:
            musics.append(item['track'])

        titles = []
        for music in musics:
            title = self.__extract_title(music)
            titles.append(title)

        return titles

    def __get_track(self, code: str) -> list:
        results = self.__api.track(code)
        name = results['name']
        artists = ''
        for artist in results['artists']:
            artists += f'{artist["name"]} '

        return [f'{name} {artists}']

    def __get_artist(self, code: str) -> list:
        results = self.__api.artist_top_tracks(code, country='BR')

        musics_titles = []
        for music in results['tracks']:
            title = self.__extract_title(music)
            musics_titles.append(title)

        return musics_titles

    def __extract_title(self, music: dict) -> str:
        title = f'{music["name"]} '
        for artist in music['artists']:
            title += f'{artist["name"]} '

        return title

    def __checkUrlValid(self, url: str) -> bool:
        try:
            type = url.split('/')[3].split('?')[0]
            code = url.split('/')[4].split('?')[0]

            if type == '' or code == '':
                return False

            return True
        except:
            return False
