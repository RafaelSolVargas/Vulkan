from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class SongsButton(Button):
    def __init__(self):
        super().__init__(label="Songs", style=ButtonStyle.secondary, emoji=VEmojis().QUEUE)

    async def callback(self, interaction: Interaction) -> None:
        pass
