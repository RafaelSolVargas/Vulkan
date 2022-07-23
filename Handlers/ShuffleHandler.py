from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import UnknownError
from Parallelism.ProcessManager import ProcessManager


class ShuffleHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = ProcessManager()
        processContext = processManager.getRunningPlayerContext(self.guild)
        if processContext:
            try:
                with processContext.getLock():
                    playlist = processContext.getPlaylist()
                    playlist.shuffle()

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
