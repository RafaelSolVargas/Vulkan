from Handlers.QueueHandler import QueueHandler
from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Music.VulkanBot import VulkanBot


class SongsButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Songs", style=ButtonStyle.secondary, emoji=VEmojis().QUEUE)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = QueueHandler(interaction, self.__bot)
        response = await handler.run()

        if response.embed:
            await interaction.followup.send(embed=response.embed)
