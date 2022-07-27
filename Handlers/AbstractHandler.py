from abc import ABC, abstractmethod
from typing import List
from discord.ext.commands import Context
from discord import Client, Guild, ClientUser, Member
from Config.Messages import Messages
from Music.VulkanBot import VulkanBot
from Handlers.HandlerResponse import HandlerResponse
from Config.Configs import Configs
from Config.Helper import Helper
from Views.Embeds import Embeds


class AbstractHandler(ABC):
    def __init__(self, ctx: Context, bot: VulkanBot) -> None:
        self.__bot: VulkanBot = bot
        self.__guild: Guild = ctx.guild
        self.__ctx: Context = ctx
        self.__bot_user: ClientUser = self.__bot.user
        self.__id = self.__bot_user.id
        self.__messages = Messages()
        self.__config = Configs()
        self.__helper = Helper()
        self.__embeds = Embeds()
        self.__bot_member: Member = self.__get_member()

    @abstractmethod
    async def run(self) -> HandlerResponse:
        pass

    @property
    def id(self) -> int:
        return self.__id

    @property
    def bot_member(self) -> Member:
        return self.__bot_member

    @property
    def bot_user(self) -> ClientUser:
        return self.__bot_user

    @property
    def guild(self) -> Guild:
        return self.__guild

    @property
    def bot(self) -> Client:
        return self.__bot

    @property
    def config(self) -> Configs:
        return self.__config

    @property
    def messages(self) -> Messages:
        return self.__messages

    @property
    def helper(self) -> Helper:
        return self.__helper

    @property
    def ctx(self) -> Context:
        return self.__ctx

    @property
    def embeds(self) -> Embeds:
        return self.__embeds

    def __get_member(self) -> Member:
        guild_members: List[Member] = self.__guild.members
        for member in guild_members:
            if member.id == self.__id:
                return member
