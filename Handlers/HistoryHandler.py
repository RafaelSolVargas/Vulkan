from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Utils.Utils import Utils
from typing import Union
from discord import Interaction


class HistoryHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        playersManager: AbstractPlayersManager = self.config.getPlayersManager()
        if playersManager.verifyIfPlayerExists(self.guild):
            playerLock = playersManager.getPlayerLock(self.guild)
            acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
            if acquired:
                history = playersManager.getPlayerPlaylist(self.guild).getSongsHistory()
                playerLock.release()
            else:
                # If the player doesn't respond in time we restart it
                playersManager.resetPlayer(self.guild, self.ctx)
                embed = self.embeds.PLAYER_RESTARTED()
                return HandlerResponse(self.ctx, embed)
        else:
            history = []

        if len(history) == 0:
            text = self.messages.HISTORY_EMPTY
        else:
            text = f'\n📜 History Length: {len(history)} | Max: {self.config.MAX_SONGS_HISTORY}\n'
            for pos, song in enumerate(history, start=1):
                text += f"**`{pos}` - ** {song.title} - `{Utils.format_time(song.duration)}`\n"

        embed = self.embeds.HISTORY(text)
        return HandlerResponse(self.ctx, embed)
