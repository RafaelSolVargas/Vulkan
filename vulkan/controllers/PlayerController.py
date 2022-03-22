from typing import Dict, List, Union
from Config.Singleton import Singleton
from discord import Guild, Client, VoiceClient
from Vulkan.Music.Player import Player


class PlayersController(Singleton):
    def __init__(self, bot: Client = None) -> None:
        if not super().created:
            self.__bot: Client = bot
            if bot is not None:
                self.__players: Dict[Guild, Player] = self.__create_players()

    def set_bot(self, bot: Client) -> None:
        self.__bot: Client = bot
        self.__players: Dict[Guild, Player] = self.__create_players()

    def get_player(self, guild: Guild) -> Player:
        if guild not in self.__players.keys():
            player = Player(self.__bot, guild)
            self.__players[guild] = player

        return self.__players[guild]

    def reset_player(self, guild: Guild) -> None:
        if isinstance(guild, Guild):
            player = Player(self.__bot, guild)
            self.__players[guild] == player

    def get_guild_voice(self, guild: Guild) -> Union[VoiceClient, None]:
        if guild.voice_client is None:
            return None
        else:
            return guild.voice_client

    def __create_players(self) -> Dict[Guild, Player]:
        list_guilds: List[Guild] = self.__bot.guilds
        players: Dict[Guild, Player] = {}

        for guild in list_guilds:
            player = Player(self.__bot, guild)
            players[guild] = player

        return players
