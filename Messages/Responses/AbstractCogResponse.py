from abc import ABC, abstractmethod
from Handlers.HandlerResponse import HandlerResponse
from discord.ext.commands import Context
from discord import Message
from Messages.MessagesCategory import MessagesCategory
from Messages.MessagesManager import MessagesManager
from Music.VulkanBot import VulkanBot


class AbstractCommandResponse(ABC):
    def __init__(self, response: HandlerResponse, category: MessagesCategory) -> None:
        self.__messagesManager = MessagesManager()
        self.__response: HandlerResponse = response
        self.__category: MessagesCategory = category
        self.__context: Context = response.ctx
        self.__message: Message = response.ctx.message
        self.__bot: VulkanBot = response.ctx.bot

    @property
    def response(self) -> HandlerResponse:
        return self.__response

    @property
    def category(self) -> MessagesCategory:
        return self.__category

    @property
    def bot(self) -> VulkanBot:
        return self.__bot

    @property
    def message(self) -> Message:
        return self.__message

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def manager(self) -> MessagesManager:
        return self.__messagesManager

    @abstractmethod
    async def run(self, deleteLast: bool = True) -> None:
        pass
