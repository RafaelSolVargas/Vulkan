from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessInfo import ProcessInfo, ProcessStatus
from Parallelism.Commands import VCommands, VCommandsType
from typing import Union
from discord import Interaction


class StopHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = self.config.getProcessManager()
        processInfo: ProcessInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            if processInfo.getStatus() == ProcessStatus.SLEEPING:
                embed = self.embeds.NOT_PLAYING()
                return HandlerResponse(self.ctx, embed)

            # Send command to player process stop
            command = VCommands(VCommandsType.STOP, None)
            queue = processInfo.getQueueToPlayer()
            queue.put(command)

            embed = self.embeds.STOPPING_PLAYER()
            return HandlerResponse(self.ctx, embed)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
