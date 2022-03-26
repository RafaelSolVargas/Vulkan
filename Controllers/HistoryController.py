from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Utils.Utils import Utils


class HistoryController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        history = self.player.playlist.songs_history

        if len(history) == 0:
            text = self.config.HISTORY_EMPTY

        else:
            text = f'\n📜 History Length: {len(history)} | Max: {self.config.MAX_SONGS_HISTORY}\n'
            for pos, song in enumerate(history, start=1):
                text += f"**`{pos}` - ** {song.title} - `{Utils.format_time(song.duration)}`\n"

        embed = self.embeds.HISTORY(text)
        return ControllerResponse(self.ctx, embed)
