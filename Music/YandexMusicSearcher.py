import yandex_music
from Config.Exceptions import YandexMusicError
from Config.Messages import YandexMusicMessage


class YandexMusicSearcher:
    def __init__(self) -> None:
        self.__messages = YandexMusicMessage()
        self.__client = yandex_music.Client().init()
        self.__acceptedTypes = ['artist', 'users', 'album']

    def search(self, url: str) -> None:
        if not self.__verifyValidUrl(url):
            raise YandexMusicError(self.__messages.INVALID_YANDEX_MUSIC_URL, self.__messages.GENERIC_TITLE)

        urlType = url.split('/')[3]

        if urlType == 'album' and 'track' in url:
            urlType = 'track'

        try:
            musics = []
            if urlType == 'album':
                album_id = url.split("/")[4]
                musics = self.__get_album(album_id)
            elif urlType == 'users':
                kind = url.split("/")[6]
                user_id = url.split("/")[4]
                musics = self.__get_playlist(kind, user_id)
            elif urlType == 'track':
                track_id = url.split("/")[6]
                musics = self.__get_track(track_id)
            elif urlType == 'artist':
                artist_id = url.split("/")[4]
                musics = self.__get_artist(artist_id)

            return musics
        except Exception as e:
            print(f'[YANDEX MUSIC ERROR] -> {e}')
            raise YandexMusicError(self.__messages.INVALID_YANDEX_MUSIC_URL, self.__messages.GENERIC_TITLE)
    
    def __get_album(self, album_id: str) -> list:
        tracks = self.__client.albums_with_tracks(album_id).volumes[0]

        return [f"{track.title} {', '.join(track.artists_name())}" for track in tracks]

    def __get_track(self, track_id: str) -> list:
        track = self.__client.tracks(track_id)[0]

        return [f"{track.title} {', '.join(track.artists_name())}"]

    def __get_playlist(self, kind: str, user_id: str) -> list:
        playlist = [track.track for track in self.__client.users_playlists(kind, user_id).tracks]

        return [f"{track.title} {', '.join(track.artists_name())}" for track in playlist]
    
    def __get_artist(self, artist_id: str, max_tracks = 2**31-1) -> list:
        tracks = self.__client.artists_tracks(artist_id, page_size=max_tracks).tracks

        return [f"{track.title} {', '.join(track.artists_name())}" for track in tracks]
            
    def __verifyValidUrl(self, url: str) ->  bool:
        try:
            urlType = url.split('/')[3]
            code = url.split('/')[4]

            if urlType  == '' or code == '':
                return False
            
            if urlType not in self.__acceptedTypes:
                return False
            
            return True
        except:
            return False
        