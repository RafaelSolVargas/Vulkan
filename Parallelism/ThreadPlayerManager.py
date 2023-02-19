from multiprocessing import Lock
from typing import Any, Dict, Union
from Config.Singleton import Singleton
from discord import Guild, Interaction, TextChannel
from discord.ext.commands import Context
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Music.Song import Song
from Music.Playlist import Playlist
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from Parallelism.ThreadPlayer import ThreadPlayer


class ThreadPlayerInfo:
    """
    Class to store the reference to all structures to maintain a player thread
    """

    def __init__(self, thread: ThreadPlayer, playlist: Playlist, lock: Lock, textChannel: TextChannel) -> None:
        self.__thread = thread
        self.__playlist = playlist
        self.__lock = lock
        self.__textChannel = textChannel

    def getPlayer(self) -> ThreadPlayer:
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
            self.__playersThreads: Dict[int, ThreadPlayerInfo] = {}

    async def sendCommandToPlayer(self, command: VCommands, guild: Guild, forceCreation: bool = False, context: Union[Context, Interaction] = None):
        playerInfo = self.__playersThreads[guild.id]
        player = playerInfo.getPlayer()
        if player is None and forceCreation:
            self.__createPlayerThreadInfo(context)
        if player is None:
            return

        await player.receiveCommand(command)

    async def __receiveCommand(self, command: VCommands, guildID: int, args: Any) -> None:
        commandType = command.getType()
        if commandType == VCommandsType.NOW_PLAYING:
            await self.showNowPlaying(guildID, args)
        else:
            print(
                f'[ERROR] -> Command not processable received from Thread {guildID}: {commandType}')

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
                if not self.__playersThreads[guild.id].getPlayer().is_alive():
                    self.__playersThreads[guild.id] = self.__recreateThread(guild, context)

            return self.__playersThreads[guild.id]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def resetPlayer(self, guild: Guild, context: Context) -> None:
        if guild.id not in self.__playersThreads.keys():
            return None

        # Recreate the thread keeping the playlist
        newPlayerInfo = self.__recreateThread(guild, context)
        newPlayerInfo.getPlayer().start()
        # Send a command to start the play again
        playCommand = VCommands(VCommandsType.PLAY)
        newPlayerInfo.getQueueToPlayer().put(playCommand)
        self.__playersThreads[guild.id] = newPlayerInfo

    def __getRunningPlayerInfo(self, guild: Guild) -> ThreadPlayerInfo:
        if guild.id not in self.__playersThreads.keys():
            print('Process Info not found')
            return None

        return self.__playersThreads[guild.id]

    def __createPlayerThreadInfo(self, context: Union[Context, Interaction]) -> ThreadPlayerInfo:
        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id

        voiceChannel = self.__bot.get_channel(voiceID)

        playlist = Playlist()
        lock = Lock()
        player = ThreadPlayer(self.__bot, context.guild, context.guild.name,
                              voiceChannel, playlist, lock, guildID, voiceID, self.__receiveCommand, self.__deleteThread)
        playerInfo = ThreadPlayerInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    def __deleteThread(self, guildID: int) -> None:
        """Tries to delete the thread and removes all the references to it"""
        playerInfo = self.__playersThreads[guildID]
        if playerInfo:
            thread = playerInfo.getPlayer()
            del thread
            self.__playersThreads.popitem(thread)

    def __recreateThread(self, guild: Guild, context: Union[Context, Interaction]) -> ThreadPlayerInfo:
        self.__stopPossiblyRunningProcess(guild)

        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id
        voiceChannel = self.__bot.get_channel(voiceID)

        playlist = self.__playersThreads[guildID].getPlaylist()
        lock = Lock()
        player = ThreadPlayer(self.__bot, context.guild, context.guild.name,
                              voiceChannel, playlist, lock, guildID, voiceID, self.__receiveCommand, self.__deleteThread)
        playerInfo = ThreadPlayerInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        commandExecutor = self.__playersCommandsExecutor[guildID]
        processInfo = self.__playersThreads[guildID]
        await commandExecutor.sendNowPlaying(processInfo, song)
