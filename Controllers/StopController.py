from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse


class StopController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if self.guild.voice_client is None:
            return ControllerResponse(self.ctx)

        if self.guild.voice_client.is_connected():
            self.player.playlist.clear()
            self.player.playlist.loop_off()
            self.guild.voice_client.stop()
            await self.guild.voice_client.disconnect()
            return ControllerResponse(self.ctx)


        