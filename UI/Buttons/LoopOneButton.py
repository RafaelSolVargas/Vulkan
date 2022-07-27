from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis


class LoopOneButton(Button):
    def __init__(self):
        super().__init__(label="Loop One", style=ButtonStyle.secondary, emoji=VEmojis().LOOP_ONE)

    async def callback(self, interaction: Interaction) -> None:
        pass
