from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Utils.Cleaner import Cleaner


class NowPlayingHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__cleaner = Cleaner()

    async def run(self) -> HandlerResponse:
        if not self.player.playing:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)

        if self.player.playlist.isLoopingOne():
            title = self.messages.ONE_SONG_LOOPING
        else:
            title = self.messages.SONG_PLAYING
        await self.__cleaner.clean_messages(self.ctx, self.config.CLEANER_MESSAGES_QUANT)

        info = self.player.playlist.getCurrentSong().info
        embed = self.embeds.SONG_INFO(info, title)
        return HandlerResponse(self.ctx, embed)
