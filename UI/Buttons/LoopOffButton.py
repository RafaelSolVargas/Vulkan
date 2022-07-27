from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class LoopOffButton(Button):
    def __init__(self):
        super().__init__(label="Loop Off", style=ButtonStyle.secondary, emoji=VEmojis().LOOP_OFF)

    async def callback(self, interaction: Interaction) -> None:
        pass
