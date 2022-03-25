from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Exceptions.Exceptions import BadCommandUsage


class LoopController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self, args: str) -> ControllerResponse:
        if args == '' or args == None:
            self.player.playlist.loop_all()
            embed = self.embeds.LOOP_ALL_ACTIVATED()
            return ControllerResponse(self.ctx, embed)

        args = args.lower()
        if self.player.playlist.current is None:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return ControllerResponse(self.ctx, embed, error)

        if args == 'one':
            self.player.playlist.loop_one()
            embed = self.embeds.LOOP_ONE_ACTIVATED()
            return ControllerResponse(self.ctx, embed)
        elif args == 'all':
            self.player.playlist.loop_all()
            embed = self.embeds.LOOP_ALL_ACTIVATED()
            return ControllerResponse(self.ctx, embed)
        elif args == 'off':
            self.player.playlist.loop_off()
            embed = self.embeds.LOOP_DISABLE()
            return ControllerResponse(self.ctx, embed)
        else:
            error = BadCommandUsage()
            embed = self.embeds.BAD_LOOP_USE()
            return ControllerResponse(self.ctx, embed, error)
