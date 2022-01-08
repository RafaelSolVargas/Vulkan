import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import config


class SpotifySearch():
    """Search a Spotify music or playlist and return the musics names"""

    def __init__(self) -> None:
        self.__connected = False
        self.__connect()

    @property
    def connected(self):
        return self.__connected

    def __connect(self) -> bool:
        try:
            # Initialize the connection with Spotify API
            self.__api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))
            self.__connected = True
            return True
        except:
            return False

    def search(self, music=str) -> list:
        """Search and return the title of musics on Spotify"""
        type = music.split('/')[3].split('?')[0]
        code = music.split('/')[4].split('?')[0]
        if type == 'album':
            musics = self.__get_album(code)
        elif type == 'playlist':
            musics = self.__get_playlist(code)
        elif type == 'track':
            musics = self.__get_track(code)
        else:
            return None

        return musics

    def __get_album(self, code=str) -> list:
        """Get the externals urls of a album

        ARG: Spotify Code of the Album
        """
        if self.__connected == True:
            try:
                results = self.__api.album_tracks(code)
                musics = results['items']

                while results['next']:  # Get the next pages
                    results = self.__api.next(results)
                    musics.extend(results['items'])

                musicsTitle = []

                for music in musics:
                    try:
                        title = self.__extract_title(music)
                        musicsTitle.append(title)
                    except:
                        pass
                return musicsTitle
            except Exception as e:
                raise e

    def __get_playlist(self, code=str) -> list:
        """Get the externals urls of a playlist

        Arg: Spotify Code of the Playlist
        """
        try:
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
                try:
                    title = self.__extract_title(music)
                    titles.append(title)
                except Exception as e:
                    raise e

            return titles

        except Exception as e:
            raise e

    def __get_track(self, code=str) -> list:
        """Convert a external_url track to the title of the music

        ARG: Spotify Code of the Music
        """
        results = self.__api.track(code)
        name = results['name']
        artists = ''
        for artist in results['artists']:
            artists += f'{artist["name"]} '

        return [f'{name} {artists}']

    def __extract_title(self, music: dict) -> str:
        """Receive a spotify music object and return his title

        ARG: music dict returned by Spotify
        """
        title = f'{music["name"]} '
        for artist in music['artists']:
            title += f'{artist["name"]} '

        return title
