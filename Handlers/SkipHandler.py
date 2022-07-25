from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import BadCommandUsage
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class SkipHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:  # Verify if there is a running process
            playlist = processInfo.getPlaylist()
            if playlist.isLoopingOne():
                embed = self.embeds.ERROR_DUE_LOOP_ONE_ON()
                error = BadCommandUsage()
                return HandlerResponse(self.ctx, embed, error)

            # Send a command to the player process to skip the music
            command = VCommands(VCommandsType.SKIP, None)
            queue = processInfo.getQueue()
            queue.put(command)

            return HandlerResponse(self.ctx)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
