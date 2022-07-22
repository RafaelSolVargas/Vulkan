import asyncio
from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Exceptions.Exceptions import UnknownError
from Music.Downloader import Downloader


class ShuffleController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__down = Downloader()

    async def run(self) -> ControllerResponse:
        try:
            self.player.playlist.shuffle()
            songs = self.player.playlist.getSongsToPreload()

            asyncio.create_task(self.__down.preload(songs))
            embed = self.embeds.SONGS_SHUFFLED()
            return ControllerResponse(self.ctx, embed)
        except Exception as e:
            print(f'DEVELOPER NOTE -> Error Shuffling: {e}')
            error = UnknownError()
            embed = self.embeds.ERROR_SHUFFLING()
            return ControllerResponse(self.ctx, embed, error)
