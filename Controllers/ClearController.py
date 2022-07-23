from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Parallelism.ProcessManager import ProcessManager


class ClearController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        # Get the current process of the guild
        processManager = ProcessManager()
        processContext = processManager.getRunningPlayerContext(self.guild)
        if processContext:
            # Clear the playlist
            playlist = processContext.getPlaylist()
            with processContext.getLock():
                playlist.clear()

        return ControllerResponse(self.ctx)
