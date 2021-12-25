import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
from config import config
import aiohttp


class Browser():
    def __init__(self) -> None:
        self.__url_regex = re.compile(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        self.__session = aiohttp.ClientSession(
            headers={'User-Agent': 'python-requests/2.20.0'})

    async def search(self, url) -> str:
        """Convert the external_url link to the title of music using browser"""
        if re.search(self.__url_regex, url):
            result = self.__url_regex.search(url)
            url = result.group(0)

        async with self.__session.get(url) as response:
            page = await response.text()
            soup = BeautifulSoup(page, 'html.parser')

            title = soup.find('title')
            title = title.string
            title = title.replace('- song by', '')
            title = title.replace('| Spotify', '')
            return title


class SpotifySearch():
    """Search a Spotify music or playlist and return the musics names"""

    def __init__(self) -> None:
        self.__connected = False
        self.__browser = Browser()

    def connect(self) -> bool:
        try:
            # Initialize the connection with Spotify API
            self.__api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))
            self.__connected = True
            return True
        except:
            return False

    def search(self, music) -> list:
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

    def __get_album(self, code) -> list:
        """Get the externals urls of a album

            ARG: Spotify Code of the Album
        """
        if self.__connected == True:
            try:
                # Load all music objects
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
            except:
                if config.SPOTIFY_ID != "" or config.SPOTIFY_SECRET != "":
                    print("ERROR: Check spotify CLIENT_ID and SECRET")

    def __get_playlist(self, code) -> list:
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
            if config.SPOTIFY_ID != "" or config.SPOTIFY_SECRET != "":
                print("ERROR: Check spotify CLIENT_ID and SECRET")
            else:
                raise e

    def __get_track(self, code) -> list:
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

    async def __convert_spotify(self, url) -> str:
        """(Experimental) - Convert the external_url link to the title of music using browser"""
        title = self.__browser(url)
        return title


if __name__ == '__main__':
    spSearch = SpotifySearch()
    spSearch.connect()

    lista = spSearch.search(
        'https://open.spotify.com/track/7wpnz7hje4FbnjZuWQtJHP')
    lista2 = spSearch.search(
        'https://open.spotify.com/album/6wEkHIUHNb1kZiV2nCnVoh')
    lista3 = spSearch.search(
        'https://open.spotify.com/playlist/5DOtjJ6rSMddAKyStv7Yc7?si=v893Wv0VSyuh0PokQvC8-g&utm_source=whatsapp')
    print(lista3)
    print(lista2)
    print(lista)
