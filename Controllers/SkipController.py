from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Exceptions.Exceptions import BadCommandUsage
from Controllers.ControllerResponse import ControllerResponse


class SkipController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if self.player.playlist.looping_one:
            embed = self.__embeds.FAIL_DUE_TO_LOOP_ON
            error = BadCommandUsage('', '')
            response = ControllerResponse(self.ctx, embed, error)
            return response

        voice = self.controller.get_guild_voice(self.guild)
        if voice is None:
            response = ControllerResponse(self.ctx)
            return response
        else:
            voice.stop()
            response = ControllerResponse(self.ctx)
            return response
