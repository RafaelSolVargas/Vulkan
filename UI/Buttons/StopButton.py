from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class StopButton(Button):
    def __init__(self):
        super().__init__(label="Stop", style=ButtonStyle.secondary, emoji=VEmojis().STOP)

    async def callback(self, interaction: Interaction) -> None:
        pass
