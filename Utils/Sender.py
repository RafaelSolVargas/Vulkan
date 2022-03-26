from discord.ext.commands import Context
from discord import Embed


class Sender:
    @classmethod
    async def send_embed(cls, ctx: Context, embed: Embed) -> None:
        pass

    @classmethod
    async def send_message(cls, ctx: Context, message: Embed) -> None:
        pass
