from abc import ABC, abstractmethod
from typing import List, Union
from discord.ext.commands import Context
from discord import Client, Guild, ClientUser, Interaction, Member, User
from Config.Messages import Messages
from Music.VulkanBot import VulkanBot
from Handlers.HandlerResponse import HandlerResponse
from Config.Configs import VConfigs
from Config.Helper import Helper
from Config.Embeds import VEmbeds


class AbstractHandler(ABC):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        self.__bot: VulkanBot = bot
        self.__guild: Guild = ctx.guild
        self.__ctx: Context = ctx
        self.__bot_user: ClientUser = self.__bot.user
        self.__id = self.__bot_user.id
        self.__messages = Messages()
        self.__config = VConfigs()
        self.__helper = Helper()
        self.__embeds = VEmbeds()
        self.__bot_member: Member = self.__get_member()
        if isinstance(ctx, Context):
            self.__author = ctx.author
        else:
            self.__author = ctx.user

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
    def author(self) -> User:
        return self.__author

    @property
    def guild(self) -> Guild:
        return self.__guild

    @property
    def bot(self) -> Client:
        return self.__bot

    @property
    def config(self) -> VConfigs:
        return self.__config

    @property
    def messages(self) -> Messages:
        return self.__messages

    @property
    def helper(self) -> Helper:
        return self.__helper

    @property
    def ctx(self) -> Union[Context, Interaction]:
        return self.__ctx

    @property
    def embeds(self) -> VEmbeds:
        return self.__embeds

    def __get_member(self) -> Member:
        guild_members: List[Member] = self.__guild.members
        for member in guild_members:
            if member.id == self.__id:
                return member
