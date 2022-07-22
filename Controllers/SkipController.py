from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Exceptions.Exceptions import BadCommandUsage
from Controllers.ControllerResponse import ControllerResponse


class SkipController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if self.player.playlist.isLoopingOne():
            embed = self.embeds.ERROR_DUE_LOOP_ONE_ON()
            error = BadCommandUsage()
            return ControllerResponse(self.ctx, embed, error)

        voice = self.controller.get_guild_voice(self.guild)
        if voice is None:
            return ControllerResponse(self.ctx)
        else:
            voice.stop()
            return ControllerResponse(self.ctx)
