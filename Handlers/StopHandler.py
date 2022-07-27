from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType
from typing import Union
from discord import Interaction


class StopHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            # Send command to player process stop
            command = VCommands(VCommandsType.STOP, None)
            queue = processInfo.getQueue()
            queue.put(command)

            return HandlerResponse(self.ctx)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
