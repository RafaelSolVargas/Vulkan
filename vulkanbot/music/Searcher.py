from vulkanbot.music.Types import Provider
from vulkanbot.music.Spotify import SpotifySearch
from vulkanbot.music.utils import is_url


class Searcher():
    """Turn the user input into list of musics names, support youtube and spotify"""

    def __init__(self) -> None:
        self.__Spotify = SpotifySearch()
        print(f'Spotify Connected: {self.__Spotify.connect()}')

    def search(self, music: str) -> list:
        """Return a list with the song names or an URL

        Arg -> User Input, a string with the 
        Return -> A list of musics names and Provider Type
        """
        url_type = self.__identify_source(music)

        if url_type == Provider.YouTube:
            return [music], Provider.YouTube

        elif url_type == Provider.Spotify:
            musics = self.__Spotify.search(music)
            return musics, Provider.Name

        elif url_type == Provider.Name:
            return [music], Provider.Name
        
        elif url_type == Provider.Unknown:
            return None, Provider.Unknown

    def __identify_source(self, music) -> Provider:
        """Identify the provider of a music"""
        if not is_url(music):
            return Provider.Name

        if "https://www.youtu" in music or "https://youtu.be" in music:
            return Provider.YouTube

        if "https://open.spotify.com" in music:
            return Provider.Spotify

        # If no match
        return Provider.Unknown

