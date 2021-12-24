from vulkanbot.music.Types import Provider
from vulkanbot.music.Spotify import SpotifySearch
from vulkanbot.music.Youtube import YoutubeSearch


class Searcher():
    """Turn the user input into list of musics names, support youtube and spotify"""

    def __init__(self) -> None:
        self.__Youtube = YoutubeSearch()
        self.__Spotify = SpotifySearch()
        print(f'Spotify Connected: {self.__Spotify.connect()}')

    def search(self, music: str) -> list:
        """Return a list with the track name of a music or playlist"""
        url_type = self.__identify_source(music)

        if url_type == Provider.Name:
            return [music]

        elif url_type == Provider.YouTube:
            musics = self.__Youtube.search(music)
            return musics

        elif url_type == Provider.Spotify:
            musics = self.__Spotify.search(music)
            return musics

    def __identify_source(self, music):
        if 'http' not in music:
            return Provider.Name

        if "https://www.youtu" in music or "https://youtu.be" in music:
            return Provider.YouTube

        if "https://open.spotify.com/track" in music:
            return Provider.Spotify

        if "https://open.spotify.com/playlist" in music or "https://open.spotify.com/album" in music:
            return Provider.Spotify_Playlist

        # If no match
        return Provider.Unknown
