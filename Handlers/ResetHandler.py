from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType
from Music.MusicBot import VulkanBot


class ResetHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            command = VCommands(VCommandsType.RESET, None)
            queue = processInfo.getQueue()
            queue.put(command)

            return HandlerResponse(self.ctx)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
