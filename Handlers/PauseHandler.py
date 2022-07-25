from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class PauseHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            # Send Pause command to be execute by player process
            command = VCommands(VCommandsType.PAUSE, None)
            queue = processInfo.getQueue()
            queue.put(command)

            return HandlerResponse(self.ctx)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
