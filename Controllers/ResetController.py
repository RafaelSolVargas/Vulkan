from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Controllers.PlayersController import PlayersController


class ResetController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__controller = PlayersController(self.bot)

    async def run(self) -> ControllerResponse:
        try:
            await self.player.force_stop()
            await self.bot_member.move_to(None)
            self.__controller.reset_player(self.guild)
            return ControllerResponse(self.ctx)
        except Exception as e:
            print(f'DEVELOPER NOTE -> Reset Error: {e}')
