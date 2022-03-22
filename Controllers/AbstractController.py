from abc import ABC, abstractmethod
from discord.ext.commands import Context
from discord import Client, Guild
from Controllers.PlayerController import PlayersController
from Music.Player import Player
from Controllers.ControllerResponse import ControllerResponse
from Config.Config import Configs
from Config.Helper import Helper
from Views.Embeds import Embeds


class AbstractController(ABC):
    def __init__(self, ctx: Context, bot: Client) -> None:
        self.__bot: Client = bot
        self.__controller = PlayersController(self.__bot)
        self.__player: Player = self.__controller.get_player(ctx.guild)
        self.__guild: Guild = ctx.guild
        self.__ctx: Context = ctx
        self.__config = Configs()
        self.__helper = Helper()
        self.__embeds = Embeds()

    @abstractmethod
    async def run(self) -> ControllerResponse:
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

    @property
    def config(self) -> Configs:
        return self.__config

    @property
    def helper(self) -> Helper:
        return self.__helper

    @property
    def ctx(self) -> Context:
        return self.__ctx

    @property
    def embeds(self) -> Embeds:
        return self.__embeds
