from vulkan.results import AbstractResult
from typing import Union
from discord.ext.commands import Context
from vulkan.controllers.Exceptions import Error


class SuccessResult(AbstractResult):
    def __init__(self) -> None:
        super().__init__()
