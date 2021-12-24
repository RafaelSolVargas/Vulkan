import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import config


class SpotifySearch():
    """Search and return musics names from Spotify"""

    def __init__(self) -> None:
        pass

    def connect(self) -> bool:
        try:
            # Initialize the connection with Spotify API
            self.__sp_api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))
            return True
        except:
            return False

    def search(self, music) -> list:
        pass
