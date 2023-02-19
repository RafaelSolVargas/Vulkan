from typing import Union
from discord import Interaction
from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.AbstractProcessManager import AbstractPlayersManager


class ClearHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        playersManager: AbstractPlayersManager = self.config.getPlayersManager()
        if playersManager.verifyIfPlayerExists(self.guild):
            # Clear the playlist
            playlist = playersManager.getPlayerPlaylist(self.guild)
            playerLock = playersManager.getPlayerLock(self.guild)
            acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
            if acquired:
                playlist.clear()
                playerLock.release()
                embed = self.embeds.PLAYLIST_CLEAR()
                return HandlerResponse(self.ctx, embed)
            else:
                playersManager.resetPlayer(self.guild, self.ctx)
                embed = self.embeds.PLAYER_RESTARTED()
                return HandlerResponse(self.ctx, embed)
