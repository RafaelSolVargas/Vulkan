from abc import ABC, abstractmethod
from Handlers.HandlerResponse import HandlerResponse
from discord.ext.commands import Context
from discord import Client, Message


class AbstractView(ABC):
    def __init__(self, response: HandlerResponse) -> None:
        self.__response: HandlerResponse = response
        self.__context: Context = response.ctx
        self.__message: Message = response.ctx.message
        self.__bot: Client = response.ctx.bot

    @property
    def response(self) -> HandlerResponse:
        return self.__response

    @property
    def bot(self) -> Client:
        return self.__bot

    @property
    def message(self) -> Message:
        return self.__message

    @property
    def context(self) -> Context:
        return self.__context

    @abstractmethod
    async def run(self) -> None:
        pass
