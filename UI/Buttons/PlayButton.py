from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class PlayButton(Button):
    def __init__(self):
        super().__init__(label="Play", style=ButtonStyle.secondary, emoji=VEmojis().PLAY)

    async def callback(self, interaction: Interaction) -> None:
        pass
