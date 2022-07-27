from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class SkipButton(Button):
    def __init__(self):
        super().__init__(label="Skip", style=ButtonStyle.secondary, emoji=VEmojis().SKIP)

    async def callback(self, interaction: Interaction) -> None:
        pass
