from discord import ButtonStyle, Interaction
from discord.ui import Button
from Config.Emojis import VEmojis
from Music.VulkanBot import VulkanBot
from Handlers.ResumeHandler import ResumeHandler


class PlayButton(Button):
    def __init__(self, bot: VulkanBot):
        super().__init__(label="Play", style=ButtonStyle.secondary, emoji=VEmojis().PLAY)
        self.__bot = bot

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        handler = ResumeHandler(interaction, self.__bot)
        response = await handler.run()

        if response.embed:
            await interaction.followup.send(embed=response.embed)
