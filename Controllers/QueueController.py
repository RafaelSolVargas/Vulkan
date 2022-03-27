import asyncio
from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Music.Downloader import Downloader
from Utils.Utils import Utils


class QueueController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__down = Downloader()

    async def run(self) -> ControllerResponse:
        if self.player.playlist.looping_one:
            song = self.player.playlist.current
            embed = self.embeds.ONE_SONG_LOOPING(song.info)
            return ControllerResponse(self.ctx, embed)

        songs_preload = self.player.playlist.songs_to_preload
        if len(songs_preload) == 0:
            embed = self.embeds.EMPTY_QUEUE()
            return ControllerResponse(self.ctx, embed)

        asyncio.create_task(self.__down.preload(songs_preload))

        if self.player.playlist.looping_all:
            title = self.messages.ALL_SONGS_LOOPING
        else:
            title = self.messages.QUEUE_TITLE

        total_time = Utils.format_time(sum([int(song.duration if song.duration else 0)
                                            for song in songs_preload]))
        total_songs = len(self.player.playlist)

        text = f'📜 Queue length: {total_songs} | ⌛ Duration: `{total_time}` downloaded  \n\n'

        for pos, song in enumerate(songs_preload, start=1):
            song_name = song.title if song.title else self.messages.SONG_DOWNLOADING
            text += f"**`{pos}` - ** {song_name} - `{Utils.format_time(song.duration)}`\n"

        embed = self.embeds.QUEUE(title, text)
        return ControllerResponse(self.ctx, embed)
