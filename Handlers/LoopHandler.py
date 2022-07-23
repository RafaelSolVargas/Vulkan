from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import BadCommandUsage


class LoopHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self, args: str) -> HandlerResponse:
        if args == '' or args is None:
            self.player.playlist.loop_all()
            embed = self.embeds.LOOP_ALL_ACTIVATED()
            return HandlerResponse(self.ctx, embed)

        args = args.lower()
        if self.player.playlist.getCurrentSong() is None:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        if args == 'one':
            self.player.playlist.loop_one()
            embed = self.embeds.LOOP_ONE_ACTIVATED()
            return HandlerResponse(self.ctx, embed)
        elif args == 'all':
            self.player.playlist.loop_all()
            embed = self.embeds.LOOP_ALL_ACTIVATED()
            return HandlerResponse(self.ctx, embed)
        elif args == 'off':
            self.player.playlist.loop_off()
            embed = self.embeds.LOOP_DISABLE()
            return HandlerResponse(self.ctx, embed)
        else:
            error = BadCommandUsage()
            embed = self.embeds.BAD_LOOP_USE()
            return HandlerResponse(self.ctx, embed, error)
