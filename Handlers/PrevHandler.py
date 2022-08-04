from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import BadCommandUsage, ImpossibleMove
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from typing import Union
from discord import Interaction


class PrevHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        if not self.__user_connected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)

        processManager = self.config.getProcessManager()
        processInfo = processManager.getOrCreatePlayerInfo(self.guild, self.ctx)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playlist = processInfo.getPlaylist()
        if len(playlist.getHistory()) == 0:
            error = ImpossibleMove()
            embed = self.embeds.NOT_PREVIOUS_SONG()
            return HandlerResponse(self.ctx, embed, error)

        if playlist.isLoopingAll() or playlist.isLoopingOne():
            error = BadCommandUsage()
            embed = self.embeds.FAIL_DUE_TO_LOOP_ON()
            return HandlerResponse(self.ctx, embed, error)

        # If not started, start the player process
        process = processInfo.getProcess()
        if not process.is_alive():
            process.start()

        # Send a prev command, together with the user voice channel
        prevCommand = VCommands(VCommandsType.PREV, self.author.voice.channel.id)
        queue = processInfo.getQueueToPlayer()
        queue.put(prevCommand)

        embed = self.embeds.RETURNING_SONG()
        return HandlerResponse(self.ctx, embed)

    def __user_connected(self) -> bool:
        if self.author.voice:
            return True
        else:
            return False
