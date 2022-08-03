from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Handlers.PauseHandler import PauseHandler
from Music.VulkanBot import VulkanBot


class PauseButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Pause", style=ButtonStyle.secondary, emoji=VEmojis().PAUSE)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = PauseHandler(interaction, self.__bot)
        response = await handler.run()

        if response and response.view is not None:
            await interaction.followup.send(embed=response.embed, view=response.view)
        elif response:
            await interaction.followup.send(embed=response.embed)
