from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class LoopAllButton(Button):
    def __init__(self):
        super().__init__(label="Loop All", style=ButtonStyle.secondary, emoji=VEmojis().LOOP_ALL)

    async def callback(self, interaction: Interaction) -> None:
        pass
