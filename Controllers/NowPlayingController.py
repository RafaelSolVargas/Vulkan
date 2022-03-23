from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse


class NowPlayingController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if not self.player.playing:
            embed = self.embeds.NOT_PLAYING()
            return ControllerResponse(self.ctx, embed)

        if self.player.playlist.looping_one:
            title = self.config.ONE_SONG_LOOPING
        else:
            title = self.config.SONG_PLAYING

        info = self.player.playlist.current.info
        embed = self.embeds.SONG_INFO(info, title)
        return ControllerResponse(self.ctx, embed)
