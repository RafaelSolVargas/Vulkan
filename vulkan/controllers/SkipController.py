from discord.ext.commands import Context
from discord import Client
from vulkan.controllers.AbstractHandler import AbstractHandler


class SkipHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> None:
        if self.player.playlist.looping_one:
            """ embed = Embed(
                title=config.SONG_PLAYER,
                description=config.LOOP_ON,
                colour=config.COLOURS['blue']
            )
            await ctx.send(embed=embed)
            return False
            """
            return None

        voice = self.controller.get_guild_voice(self.guild)
        if voice is None:
            return None
        else:
            voice.stop()
