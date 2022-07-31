from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessInfo import ProcessInfo, ProcessStatus
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from typing import Union
from discord import Interaction


class ResetHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        processManager = self.config.getProcessManager()
        processInfo: ProcessInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            if processInfo.getStatus() == ProcessStatus.SLEEPING:
                embed = self.embeds.NOT_PLAYING()
                return HandlerResponse(self.ctx, embed)

            command = VCommands(VCommandsType.RESET, None)
            queue = processInfo.getQueueToPlayer()
            queue.put(command)

            return HandlerResponse(self.ctx)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
