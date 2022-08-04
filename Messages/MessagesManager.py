from typing import Dict, List
from discord import Message
from Config.Singleton import Singleton
from Messages.MessagesCategory import MessagesCategory


class MessagesManager(Singleton):
    def __init__(self) -> None:
        if not super().created:
            # For each guild, and for each category, there will be a list of messages
            self.__guildsMessages: Dict[int, Dict[MessagesCategory, List[Message]]] = {}

    def addMessage(self, guildID: int, category: MessagesCategory, message: Message) -> None:
        if message is None:
            return

        # If guild not exists create Dict
        if guildID not in self.__guildsMessages.keys():
            self.__guildsMessages[guildID] = {}
        # If category not in guild yet, add
        if category not in self.__guildsMessages[guildID].keys():
            self.__guildsMessages[guildID][category] = []

        sendedMessages = self.__guildsMessages[guildID][category]
        sendedMessages.append(message)

    async def addMessageAndClearPrevious(self, guildID: int, category: MessagesCategory, message: Message) -> None:
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

    async def clearMessagesOfCategory(self, guildID: int, category: MessagesCategory) -> None:
        sendedMessages = self.__guildsMessages[guildID][category]

        for message in sendedMessages:
            self.__deleteMessage(message)

    async def clearMessagesOfGuild(self, guildID: int) -> None:
        categoriesMessages = self.__guildsMessages[guildID]

        for category in categoriesMessages.keys():
            for message in categoriesMessages[category]:
                self.__deleteMessage(message)

    async def __deleteMessage(self, message: Message) -> None:
        try:
            await message.delete()
        except Exception as e:
            print(f'[ERROR DELETING MESSAGE] -> {e}')
            pass
