import deezer
from Config.Exceptions import DeezerError
from Config.Messages import DeezerMessages


class DeezerSearcher:
    def __init__(self) -> None:
        self.__client = deezer.Client()
        self.__messages = DeezerMessages()
        self.__acceptedTypes = ['track', 'artist', 'playlist', 'album']

    def search(self, url: str) -> None:
        if not self.__verifyValidUrl(url):
            raise DeezerError(self.__messages.INVALID_DEEZER_URL, self.__messages.GENERIC_TITLE)

        urlType = url.split('/')[4].split('?')[0]
        code = int(url.split('/')[5].split('?')[0])

        try:
            musics = []
            if urlType == 'album':
                musics = self.__get_album(code)
            elif urlType == 'playlist':
                musics = self.__get_playlist(code)
            elif urlType == 'track':
                musics = self.__get_track(code)
            elif urlType == 'artist':
                musics = self.__get_artist(code)

            return musics
        except Exception as e:
            print(f'[DEEZER ERROR] -> {e}')
            raise DeezerError(self.__messages.INVALID_DEEZER_URL, self.__messages.GENERIC_TITLE)

    def __get_album(self, code: int) -> list:
        album = self.__client.get_album(code)

        return [track.title for track in album.tracks]

    def __get_track(self, code: int) -> list:
        track = self.__client.get_track(code)

        return [track.title]

    def __get_playlist(self, code: int) -> list:
        playlist = self.__client.get_playlist(code)

        return [track.title for track in playlist.tracks]

    def __get_artist(self, code: int) -> list:
        artist = self.__client.get_artist(code)

        topMusics = artist.get_top()

        return [track.title for track in topMusics]

    def __verifyValidUrl(self, url: str) -> bool:
        try:
            urlType = url.split('/')[4].split('?')[0]
            code = url.split('/')[5].split('?')[0]

            code = int(code)

            if urlType == '' or code == '':
                return False

            if urlType not in self.__acceptedTypes:
                return False

            return True
        except:
            return False
