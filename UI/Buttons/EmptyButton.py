from typing import Awaitable
from discord import ButtonStyle, Interaction
from discord.ui import Button
from Handlers.HandlerResponse import HandlerResponse
from Music.VulkanBot import VulkanBot


class EmptyButton(Button):
    def __init__(self, bot: VulkanBot, cb: Awaitable, emoji, label=None, *args, **kwargs):
        super().__init__(label=label, style=ButtonStyle.secondary, emoji=emoji)
        self.__bot = bot
        self.__args = args
        self.__kwargs = kwargs
        self.__callback = cb

    async def callback(self, interaction: Interaction) -> None:
        """Callback to when Button is clicked"""
        # Return to Discord that this command is being processed
        await interaction.response.defer()

        response: HandlerResponse = await self.__callback(*self.__args, **self.__kwargs)

        if response and response.view is not None:
            await interaction.followup.send(embed=response.embed, view=response.view)
        elif response:
            await interaction.followup.send(embed=response.embed)
