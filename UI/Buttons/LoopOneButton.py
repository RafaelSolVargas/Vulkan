from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Handlers.LoopHandler import LoopHandler
from Music.VulkanBot import VulkanBot


class LoopOneButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Loop One", style=ButtonStyle.secondary, emoji=VEmojis().LOOP_ONE)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = LoopHandler(interaction, self.__bot)
        response = await handler.run('one')

        if response and response.view is not None:
            await interaction.followup.send(embed=response.embed, view=response.view)
        elif response:
            await interaction.followup.send(embed=response.embed)
