from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Handlers.PrevHandler import PrevHandler
from Music.VulkanBot import VulkanBot


class BackButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Back", style=ButtonStyle.secondary, emoji=VEmojis().BACK)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = PrevHandler(interaction, self.__bot)
        response = await handler.run()
        print(response)
        print(response.success)
        print(response.error)
        print(response.error)
        print(response.embed)
        if response.embed:
            await interaction.followup.send(embed=response.embed)
