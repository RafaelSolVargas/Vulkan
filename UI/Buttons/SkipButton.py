from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Music.VulkanBot import VulkanBot
from Handlers.SkipHandler import SkipHandler


class SkipButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Skip", style=ButtonStyle.secondary, emoji=VEmojis().SKIP)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = SkipHandler(interaction, self.__bot)
        response = await handler.run()

        if response and response.view is not None:
            await interaction.followup.send(embed=response.embed, view=response.view)
        elif response:
            await interaction.followup.send(embed=response.embed)
