from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import BadCommandUsage
from typing import Union
from discord import Interaction


class LoopHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, args: str) -> HandlerResponse:
        # Get the current process of the guild
        processManager = self.config.getProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playlist = processInfo.getPlaylist()

        processLock = processInfo.getLock()
        acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        if acquired:
            if args == '' or args is None:
                playlist.loop_all()
                embed = self.embeds.LOOP_ALL_ACTIVATED()
                processLock.release()
                return HandlerResponse(self.ctx, embed)

            args = args.lower()
            error = None
            if playlist.getCurrentSong() is None:
                embed = self.embeds.NOT_PLAYING()
                error = BadCommandUsage()
                return HandlerResponse(self.ctx, embed, error)

            if args == 'one':
                playlist.loop_one()
                embed = self.embeds.LOOP_ONE_ACTIVATED()
            elif args == 'all':
                playlist.loop_all()
                embed = self.embeds.LOOP_ALL_ACTIVATED()
            elif args == 'off':
                playlist.loop_off()
                embed = self.embeds.LOOP_DISABLE()
            else:
                error = BadCommandUsage()
                embed = self.embeds.BAD_LOOP_USE()

            processLock.release()
            return HandlerResponse(self.ctx, embed, error)
        else:
            processManager.resetProcess(self.guild, self.ctx)
            embed = self.embeds.PLAYER_RESTARTED()
            return HandlerResponse(self.ctx, embed)
