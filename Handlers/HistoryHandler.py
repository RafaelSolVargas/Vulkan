from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Utils.Utils import Utils
from Parallelism.ProcessManager import ProcessManager


class HistoryHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if processInfo:
            with processInfo.getLock():
                playlist = processInfo.getPlaylist()
                history = playlist.getSongsHistory()
        else:
            history = []

        if len(history) == 0:
            text = self.messages.HISTORY_EMPTY
        else:
            text = f'\n📜 History Length: {len(history)} | Max: {self.config.MAX_SONGS_HISTORY}\n'
            for pos, song in enumerate(history, start=1):
                text += f"**`{pos}` - ** {song.title} - `{Utils.format_time(song.duration)}`\n"

        embed = self.embeds.HISTORY(text)
        return HandlerResponse(self.ctx, embed)
