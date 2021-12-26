import discord
import datetime
from config import config


class Song():
    """Store the usefull information about a Song"""

    def __init__(self, info: dict) -> None:
        if type(info) != dict:
            return

        self.__usefull_keys = ['url', 'title', 'duration',
                               'description', 'webpage_url',
                               'channel', 'id', 'uploader',
                               'thumbnail']
        self.__extract_info(info)

    def __extract_info(self, info):
        """Extract the usefull information returned by the Downloader"""
        self.__info = {}
        for key in self.__usefull_keys:
            try:
                self.__info[key] = info[key]
            except Exception as e:
                print(e)
                raise e

    @property
    def info(self):
        """Return the compiled info of this song"""
        return self.__info

    @property
    def title(self):
        return self.__info['title']

    @property
    def source(self):
        """Return the Song Source URL to play"""
        return self.__info['url']

    def embed(self):
        """Configure and return the embed to show this song in discord chat"""
        embed = discord.Embed(title='Music Playing',
                              description=f"[{self.__info['title']}]({self.__info['webpage_url']})",
                              color=config.COLOURS['blue'])

        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)

        embed.add_field(name=config.SONGINFO_UPLOADER,
                        value=self.__info['uploader'],
                        inline=False)

        if self.duration is not None:
            duration = str(datetime.timedelta(seconds=self.__info['duration']))

            embed.add_field(name=config.SONGINFO_DURATION,
                            value=f"{duration}",
                            inline=False)

        else:
            embed.add_field(name=config.SONGINFO_DURATION,
                            value=config.SONGINFO_UNKNOWN_DURATION,
                            inline=False)

        return embed
