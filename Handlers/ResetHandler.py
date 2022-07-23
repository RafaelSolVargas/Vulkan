from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Handlers.PlayersController import PlayersController


class ResetHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__controller = PlayersController(self.bot)

    async def run(self) -> HandlerResponse:
        try:
            await self.player.force_stop()
            await self.bot_member.move_to(None)
            self.__controller.reset_player(self.guild)
            return HandlerResponse(self.ctx)
        except Exception as e:
            print(f'DEVELOPER NOTE -> Reset Error: {e}')
