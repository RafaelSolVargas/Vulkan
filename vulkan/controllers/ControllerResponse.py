from typing import Union
from discord.ext.commands import Context
from Vulkan.Exceptions.Exceptions import Error
from discord import Embed


class ControllerResponse:
    def __init__(self, ctx: Context, embed: Embed = None, error: Error = None) -> None:
        self.__ctx: Context = ctx
        self.__error: Error = error
        self.__embed: Embed = embed
        self.__success = False if error else True

    @property
    def ctx(self) -> Context:
        return self.__ctx

    @property
    def embed(self) -> Union[Embed, None]:
        return self.__embed

    def error(self) -> Union[Error, None]:
        return self.__error

    @property
    def success(self) -> bool:
        return self.__success
