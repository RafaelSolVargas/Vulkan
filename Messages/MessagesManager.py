from typing import Dict, List
from Config.Singleton import Singleton
from UI.Views.AbstractView import AbstractView
from Messages.MessagesCategory import MessagesCategory
from Messages.DiscordMessages import VAbstractMessage
import traceback


class MessagesManager(Singleton):
    def __init__(self) -> None:
        if not super().created:
            # For each guild, and for each category, there will be a list of messages
            self.__guildsMessages: Dict[int, Dict[MessagesCategory, List[VAbstractMessage]]] = {}
            # Will, for each message, store the AbstractView that controls it
            self.__messagesViews: Dict[VAbstractMessage, AbstractView] = {}

    def addMessage(self, guildID: int, category: MessagesCategory, message: VAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # If guild not exists create Dict
        if guildID not in self.__guildsMessages.keys():
            self.__guildsMessages[guildID] = {}
        # If category not in guild yet, add
        if category not in self.__guildsMessages[guildID].keys():
            self.__guildsMessages[guildID][category] = []

        sendedMessages = self.__guildsMessages[guildID][category]
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view
        sendedMessages.append(message)

    async def addMessageAndClearPrevious(self, guildID: int, category: MessagesCategory, message: VAbstractMessage, view: AbstractView = None) -> None:
        if message is None:
            return

        # If guild not exists create Dict
        if guildID not in self.__guildsMessages.keys():
            self.__guildsMessages[guildID] = {}
        # If category not in guild yet, add
        if category not in self.__guildsMessages[guildID].keys():
            self.__guildsMessages[guildID][category] = []

        sendedMessages = self.__guildsMessages[guildID][category]

        # Delete sended all messages of this category
        for previousMessage in sendedMessages:
            await self.__deleteMessage(previousMessage)

        # Create a new list with only the new message
        self.__guildsMessages[guildID][category] = [message]

        # Store the view of this message
        if view is not None and isinstance(view, AbstractView):
            self.__messagesViews[message] = view

    async def clearMessagesOfCategory(self, guildID: int, category: MessagesCategory) -> None:
        sendedMessages = self.__guildsMessages[guildID][category]

        for message in sendedMessages:
            self.__deleteMessage(message)

    async def clearMessagesOfGuild(self, guildID: int) -> None:
        categoriesMessages = self.__guildsMessages[guildID]

        for category in categoriesMessages.keys():
            for message in categoriesMessages[category]:
                self.__deleteMessage(message)

    async def __deleteMessage(self, message: VAbstractMessage) -> None:
        try:
            # If there is a view for this message delete the key
            if message in self.__messagesViews.keys():
                messageView = self.__messagesViews.pop(message)
                messageView.stopView()
                del messageView

            await message.delete()
        except Exception:
            print(f'[ERROR DELETING MESSAGE] -> {traceback.format_exc()}')
