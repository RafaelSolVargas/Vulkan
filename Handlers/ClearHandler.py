from typing import Union
from discord import Interaction
from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessInfo import ProcessInfo


class ClearHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        processManager = self.config.getProcessManager()
        processInfo: ProcessInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            # Clear the playlist
            playlist = processInfo.getPlaylist()
            processLock = processInfo.getLock()
            acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
            if acquired:
                playlist.clear()
                processLock.release()
                embed = self.embeds.PLAYLIST_CLEAR()
                return HandlerResponse(self.ctx, embed)
            else:
                processManager.resetProcess(self.guild, self.ctx)
                embed = self.embeds.PLAYER_RESTARTED()
                return HandlerResponse(self.ctx, embed)
