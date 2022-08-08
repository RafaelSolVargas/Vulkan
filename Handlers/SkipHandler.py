from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import BadCommandUsage, ImpossibleMove
from Handlers.HandlerResponse import HandlerResponse
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessInfo import ProcessInfo, ProcessStatus
from Parallelism.Commands import VCommands, VCommandsType
from typing import Union
from discord import Interaction


class SkipHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        if not self.__user_connected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)

        processManager = self.config.getProcessManager()
        processInfo: ProcessInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:  # Verify if there is a running process
            if processInfo.getStatus() == ProcessStatus.SLEEPING:
                embed = self.embeds.NOT_PLAYING()
                return HandlerResponse(self.ctx, embed)

            # Send a command to the player process to skip the music
            command = VCommands(VCommandsType.SKIP, None)
            queue = processInfo.getQueueToPlayer()
            queue.put(command)

            embed = self.embeds.SKIPPING_SONG()
            return HandlerResponse(self.ctx, embed)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)

    def __user_connected(self) -> bool:
        if self.author.voice:
            return True
        else:
            return False
