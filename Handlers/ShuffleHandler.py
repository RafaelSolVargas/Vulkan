from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import UnknownError
from Music.VulkanBot import VulkanBot
from typing import Union
from discord import Interaction

from Parallelism.AbstractProcessManager import AbstractPlayersManager


class ShuffleHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        playersManager: AbstractPlayersManager = self.config.getPlayersManager()
        if playersManager.verifyIfPlayerExists(self.guild):
            try:
                playerLock = playersManager.getPlayerLock(self.guild)
                acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
                if acquired:
                    playlist = playersManager.getPlayerPlaylist(self.guild)
                    playlist.shuffle()
                    # Release the acquired Lock
                    playerLock.release()
                else:
                    playersManager.resetPlayer(self.guild, self.ctx)
                    embed = self.embeds.PLAYER_RESTARTED()
                    return HandlerResponse(self.ctx, embed)

                embed = self.embeds.SONGS_SHUFFLED()
                return HandlerResponse(self.ctx, embed)

            except Exception as e:
                print(f'DEVELOPER NOTE -> Error Shuffling: {e}')
                error = UnknownError()
                embed = self.embeds.ERROR_SHUFFLING()

                return HandlerResponse(self.ctx, embed, error)
        else:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)
