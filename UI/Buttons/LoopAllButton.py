from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Handlers.LoopHandler import LoopHandler
from Music.VulkanBot import VulkanBot


class LoopAllButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Loop All", style=ButtonStyle.secondary, emoji=VEmojis().LOOP_ALL)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = LoopHandler(interaction, self.__bot)
        response = await handler.run('all')

        if response.embed:
            await interaction.followup.send(embed=response.embed)
