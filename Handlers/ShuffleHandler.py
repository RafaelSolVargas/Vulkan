import asyncio
from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import UnknownError
from Music.Downloader import Downloader


class ShuffleHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__down = Downloader()

    async def run(self) -> HandlerResponse:
        try:
            self.player.playlist.shuffle()
            songs = self.player.playlist.getSongsToPreload()

            asyncio.create_task(self.__down.preload(songs))
            embed = self.embeds.SONGS_SHUFFLED()
            return HandlerResponse(self.ctx, embed)
        except Exception as e:
            print(f'DEVELOPER NOTE -> Error Shuffling: {e}')
            error = UnknownError()
            embed = self.embeds.ERROR_SHUFFLING()
            return HandlerResponse(self.ctx, embed, error)
