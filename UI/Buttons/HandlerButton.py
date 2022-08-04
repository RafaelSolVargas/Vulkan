from Config.Emojis import VEmojis
from discord import ButtonStyle, Interaction, Message, TextChannel
from discord.ui import Button
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Messages.MessagesManager import MessagesManager


class HandlerButton(Button):
    """Button that will create and execute a Handler Object when clicked"""

    def __init__(self, bot: VulkanBot, handler: type[AbstractHandler], emoji: VEmojis, textChannel: TextChannel, guildID: int, category: MessagesCategory, label=None, *args, **kwargs):
        super().__init__(label=label, style=ButtonStyle.secondary, emoji=emoji)
        self.__messagesManager = MessagesManager()
        self.__category = category
        self.__guildID = guildID
        self.__channel = textChannel
        self.__bot = bot
        self.__args = args
        self.__kwargs = kwargs
        self.__handlerClass = handler

    async def callback(self, interaction: Interaction) -> None:
        """Callback to when Button is clicked"""
        # Return to Discord that this command is being processed
        await interaction.response.defer()

        # Create the handler object
        handler = self.__handlerClass(interaction, self.__bot)
        response: HandlerResponse = await handler.run(*self.__args, **self.__kwargs)

        if response and response.view is not None:
            message: Message = await self.__channel.send(embed=response.embed, view=response.view)
        else:
            message: Message = await self.__channel.send(embed=response.embed)

        # Clear the last category sended message and add the new one
        await self.__messagesManager.addMessageAndClearPrevious(self.__guildID, self.__category, message)
