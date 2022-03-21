from abc import ABC, abstractmethod
from discord.ext.commands import Context
from discord import Client, Guild
from vulkan.controllers.PlayerController import PlayersController
from vulkan.music.Player import Player
from vulkan.results.AbstractResult import AbstractResult


class AbstractHandler(ABC):
    def __init__(self, ctx: Context, bot: Client) -> None:
        self.__bot: Client = bot
        self.__controller = PlayersController(self.__bot)
        self.__player: Player = self.__controller.get_player(ctx.guild)
        self.__guild: Guild = ctx.guild

    @abstractmethod
    async def run(self) -> AbstractResult:
        pass

    @property
    def guild(self) -> Guild:
        return self.__guild

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def controller(self) -> PlayersController:
        return self.__controller

    @property
    def bot(self) -> Client:
        return self.__bot
