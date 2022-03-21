from abc import ABC, abstractmethod

from numpy import result_type
from vulkan.results.AbstractResult import AbstractResult
from discord.ext.commands import Context
from discord import Client, Message


class AbstractView(ABC):
    def __init__(self, result: AbstractResult) -> None:
        self.__result: AbstractResult = result
        self.__context: Context = result.ctx
        self.__message: Message = result.ctx.message
        self.__bot: Client = result.ctx.bot

    @property
    def result(self) -> AbstractResult:
        return self.__result

    @property
    def bot(self) -> Client:
        return self.__result.ctx.bot

    @property
    def message(self) -> Message:
        return self.__message

    @property
    def context(self) -> Context:
        return self.__context

    @abstractmethod
    def run(self) -> None:
        pass
