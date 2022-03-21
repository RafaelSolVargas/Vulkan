from typing import Union
from discord.ext.commands import Context
from vulkan.controllers.Exceptions import Error


class AbstractResult:
    def __init__(self, ctx: Context, success: bool) -> None:
        self.__success: bool = success
        self.__ctx: Context = ctx

    @property
    def ctx(self) -> Context:
        return self.__ctx

    @property
    def success(self) -> bool:
        return self.__success

    def error(self) -> Union[Error, None]:
        pass
