from discord.embeds import Embed


class Song():
    """Store the usefull information about a Song"""

    def __init__(self, url: str, title: str) -> None:
        """Create a song with only the URL to the youtube song"""
        self.__url = url
        self.__title = title
        self.__info = {}

    def finish_down(self, info: dict) -> None:
        """Get and store the full information of the song"""
        self.__usefull_keys = ['url', 'duration',
                               'description', 'webpage_url',
                               'channel', 'id', 'uploader',
                               'thumbnail']
        self.__extract_info(info)

    def __extract_info(self, info) -> None:
        """Extract the usefull information returned by the Downloader"""
        for key in self.__usefull_keys:
            try:
                self.__info[key] = info[key]
            except Exception as e:
                print(e)
                raise e

    def embed(self) -> Embed:
        """Configure and return the info to create the embed for this song"""
        info = {
            'title': self.__title,
            'url': self.__url,
            'uploader': self.__info['uploader']
        }

        if 'thumbnail' in self.__info.keys():
            info['thumbnail'] = self.__info['thumbnail']

        if 'duration' in self.__info.keys():
            info['duration'] = self.__info['duration']

        return info

    @property
    def info(self) -> dict:
        """Return the compiled info of this song"""
        if self.__info:
            return self.__info

    @property
    def title(self) -> str:
        return self.__title

    @property
    def source(self) -> str:
        """Return the Song Source URL to play"""
        if 'url' in self.__info.keys():
            return self.__info['url']

    @property
    def url(self) -> str:
        return self.__url
