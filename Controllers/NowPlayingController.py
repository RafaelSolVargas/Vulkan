from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Utils.Cleaner import Cleaner


class NowPlayingController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__cleaner = Cleaner()

    async def run(self) -> ControllerResponse:
        if not self.player.playing:
            embed = self.embeds.NOT_PLAYING()
            return ControllerResponse(self.ctx, embed)

        if self.player.playlist.isLoopingOne():
            title = self.messages.ONE_SONG_LOOPING
        else:
            title = self.messages.SONG_PLAYING
        await self.__cleaner.clean_messages(self.ctx, self.config.CLEANER_MESSAGES_QUANT)

        info = self.player.playlist.getCurrentSong().info
        embed = self.embeds.SONG_INFO(info, title)
        return ControllerResponse(self.ctx, embed)
