from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse


class ResumeController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if self.guild.voice_client is not None:
            if self.guild.voice_client.is_paused():
                self.guild.voice_client.resume()

        return ControllerResponse(self.ctx)
