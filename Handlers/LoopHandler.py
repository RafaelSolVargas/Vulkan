from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import BadCommandUsage
from Parallelism.ProcessManager import ProcessManager


class LoopHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self, args: str) -> HandlerResponse:
        # Get the current process of the guild
        processManager = ProcessManager()
        processContext = processManager.getRunningPlayerContext(self.guild)
        if not processContext:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playlist = processContext.getPlaylist()

        with processContext.getLock():
            if args == '' or args is None:
                playlist.loop_all()
                embed = self.embeds.LOOP_ALL_ACTIVATED()
                return HandlerResponse(self.ctx, embed)

            args = args.lower()
            if playlist.getCurrentSong() is None:
                embed = self.embeds.NOT_PLAYING()
                error = BadCommandUsage()
                return HandlerResponse(self.ctx, embed, error)

            if args == 'one':
                playlist.loop_one()
                embed = self.embeds.LOOP_ONE_ACTIVATED()
                return HandlerResponse(self.ctx, embed)
            elif args == 'all':
                playlist.loop_all()
                embed = self.embeds.LOOP_ALL_ACTIVATED()
                return HandlerResponse(self.ctx, embed)
            elif args == 'off':
                playlist.loop_off()
                embed = self.embeds.LOOP_DISABLE()
                return HandlerResponse(self.ctx, embed)
            else:
                error = BadCommandUsage()
                embed = self.embeds.BAD_LOOP_USE()
                return HandlerResponse(self.ctx, embed, error)
