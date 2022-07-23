from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Exceptions.Exceptions import BadCommandUsage
from Controllers.ControllerResponse import ControllerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class SkipController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        processManager = ProcessManager()
        processContext = processManager.getRunningPlayerContext(self.guild)
        if processContext:  # Verify if there is a running process
            playlist = processContext.getPlaylist()
            if playlist.isLoopingOne():
                embed = self.embeds.ERROR_DUE_LOOP_ONE_ON()
                error = BadCommandUsage()
                return ControllerResponse(self.ctx, embed, error)

            # Send a command to the player process to skip the music
            command = VCommands(VCommandsType.SKIP, None)
            queue = processContext.getQueue()
            queue.put(command)
        return ControllerResponse(self.ctx)
