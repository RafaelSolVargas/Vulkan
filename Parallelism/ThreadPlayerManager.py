from multiprocessing import Lock
from typing import Dict, Union
from Config.Singleton import Singleton
from discord import Guild, Interaction, TextChannel
from discord.ext.commands import Context
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Music.Song import Song
from Music.Playlist import Playlist
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from Parallelism.PlayerThread import PlayerThread


class PlayerThreadInfo:
    """
    Class to store the reference to all structures to maintain a player thread
    """

    def __init__(self, thread: PlayerThread, playlist: Playlist, lock: Lock, textChannel: TextChannel) -> None:
        self.__thread = thread
        self.__playlist = playlist
        self.__lock = lock
        self.__textChannel = textChannel

    def getThread(self) -> PlayerThread:
        return self.__thread

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> Lock:
        return self.__lock

    def getTextChannel(self) -> TextChannel:
        return self.__textChannel


class ThreadPlayerManager(Singleton, AbstractPlayersManager):
    """
    Manage all running player threads, creating and storing them for future calls
    """

    def __init__(self, bot: VulkanBot = None) -> None:
        if not super().created:
            self.__bot = bot
            self.__playersThreads: Dict[int, PlayerThreadInfo] = {}

    def sendCommandToPlayer(self, command: VCommands, guild: Guild, forceCreation: bool = False, context: Union[Context, Interaction] = None):
        return super().sendCommandToPlayer(command, guild, forceCreation, context)

    def getPlayerPlaylist(self, guild: Guild) -> Playlist:
        playerInfo = self.__getRunningPlayerInfo(guild)
        if playerInfo:
            return playerInfo.getPlaylist()

    def getPlayerLock(self, guild: Guild) -> Lock:
        playerInfo = self.__getRunningPlayerInfo(guild)
        if playerInfo:
            return playerInfo.getLock()

    def verifyIfPlayerExists(self, guild: Guild) -> bool:
        return guild.id in self.__playersThreads.keys()

    def createPlayerForGuild(self, guild: Guild, context: Union[Context, Interaction]):
        try:
            if guild.id not in self.__playersThreads.keys():
                self.__playersThreads[guild.id] = self.__createPlayerThreadInfo(context)
            else:
                # If the thread has ended create a new one
                if not self.__playersThreads[guild.id].getThread().is_alive():
                    self.__playersThreads[guild.id] = self.__recreateThread(guild, context)

            return self.__playersThreads[guild.id]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def resetPlayer(self, guild: Guild, context: Context) -> None:
        if guild.id not in self.__playersThreads.keys():
            return None

        # Recreate the thread keeping the playlist
        newPlayerInfo = self.__recreateThread(guild, context)
        newPlayerInfo.getThread().start()
        # Send a command to start the play again
        playCommand = VCommands(VCommandsType.PLAY)
        newPlayerInfo.getQueueToPlayer().put(playCommand)
        self.__playersThreads[guild.id] = newPlayerInfo

    def __getRunningPlayerInfo(self, guild: Guild) -> PlayerThreadInfo:
        if guild.id not in self.__playersThreads.keys():
            print('Process Info not found')
            return None

        return self.__playersThreads[guild.id]

    def __createPlayerThreadInfo(self, context: Union[Context, Interaction]) -> PlayerThreadInfo:
        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id

        playlist = Playlist()
        lock = Lock()
        player = PlayerThread(context.guild.name, playlist, lock, guildID, voiceID)
        playerInfo = PlayerThreadInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    def __recreateThread(self, guild: Guild, context: Union[Context, Interaction]) -> PlayerThreadInfo:
        self.__stopPossiblyRunningProcess(guild)

        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id

        playlist = self.__playersThreads[guildID].getPlaylist()
        lock = Lock()
        player = PlayerThread(context.guild.name, playlist, lock, guildID, voiceID)
        playerInfo = PlayerThreadInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        commandExecutor = self.__playersCommandsExecutor[guildID]
        processInfo = self.__playersThreads[guildID]
        await commandExecutor.sendNowPlaying(processInfo, song)
