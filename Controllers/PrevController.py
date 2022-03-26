from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Exceptions.Exceptions import ImpossibleMove, UnknownError
from Controllers.ControllerResponse import ControllerResponse


class PrevController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        if len(self.player.playlist.history()) == 0:
            error = ImpossibleMove()
            embed = self.embeds.NOT_PREVIOUS_SONG()
            return ControllerResponse(self.ctx, embed, error)

        if not self.__user_connected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return ControllerResponse(self.ctx, embed, error)

        if not self.__is_connected():
            success = await self.__connect()
            if not success:
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()
                return ControllerResponse(self.ctx, embed, error)

        await self.player.play_prev(self.ctx)

    def __user_connected(self) -> bool:
        if self.ctx.author.voice:
            return True
        else:
            return False

    def __is_connected(self) -> bool:
        try:
            voice_channel = self.guild.voice_client.channel

            if not self.guild.voice_client.is_connected():
                return False
            else:
                return True
        except:
            return False

    async def __connect(self) -> bool:
        # if self.guild.voice_client is None:
        try:
            await self.ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            return True
        except:
            return False
