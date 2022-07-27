from typing import Optional
from discord.ui import View, Button, button
from Config.Emojis import VEmojis
from discord import Interaction, ButtonStyle

emojis = VEmojis()


class PlayerView(View):
    def __init__(self, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

    @button(label="Back", style=ButtonStyle.secondary, emoji=emojis.BACK)
    async def prevCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Pause", style=ButtonStyle.secondary, emoji=emojis.PAUSE)
    async def pauseCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Play", style=ButtonStyle.secondary, emoji=emojis.PLAY)
    async def playCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Stop", style=ButtonStyle.secondary, emoji=emojis.STOP)
    async def stopCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Skip", style=ButtonStyle.secondary, emoji=emojis.SKIP)
    async def skipCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Songs", style=ButtonStyle.secondary, emoji=emojis.QUEUE)
    async def songsCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Loop Off", style=ButtonStyle.grey, emoji=emojis.LOOP_OFF)
    async def loopOffCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Loop All", style=ButtonStyle.secondary, emoji=emojis.LOOP_ALL)
    async def loopAllCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")

    @button(label="Loop One", style=ButtonStyle.secondary, emoji=emojis.LOOP_ONE)
    async def loopOneCallback(self, button: Button, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello")
