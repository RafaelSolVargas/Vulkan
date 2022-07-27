from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class PauseButton(Button):
    def __init__(self):
        super().__init__(label="Pause", style=ButtonStyle.secondary, emoji=VEmojis().PAUSE)

    async def callback(self, interaction: Interaction) -> None:
        pass
