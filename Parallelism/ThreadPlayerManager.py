from threading import RLock
from typing import Any, Dict, Union
from Config.Singleton import Singleton
from discord import Guild, Interaction, TextChannel
from discord.ext.commands import Context
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Music.Song import Song
from Music.Playlist import Playlist
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessExecutor import ProcessCommandsExecutor
from Parallelism.ThreadPlayer import ThreadPlayer


class ThreadPlayerInfo:
    """
    Class to store the reference to all structures to maintain a player thread
    """

    def __init__(self, thread: ThreadPlayer, playlist: Playlist, lock: RLock, textChannel: TextChannel) -> None:
        self.__thread = thread
        self.__playlist = playlist
        self.__lock = lock
        self.__textChannel = textChannel

    def getPlayer(self) -> ThreadPlayer:
        return self.__thread

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> RLock:
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

    async def sendCommandToPlayer(self, command: VCommands, guild: Guild, context: Union[Context, Interaction], forceCreation: bool = False):
        playerInfo = self.__playersThreads[guild.id]
        player = playerInfo.getPlayer()
        if player is None and forceCreation:
            self.__createPlayerThreadInfo(context)
        if player is None:
            return

        await player.receiveCommand(command)

    async def __receiveCommand(self, command: VCommands, guild: Guild, args: Any) -> None:
        commandType = command.getType()
        if commandType == VCommandsType.NOW_PLAYING:
            await self.showNowPlaying(guild, args)
        else:
            print(
                f'[ERROR] -> Command not processable received from Thread {guild.name}: {commandType}')

    def getPlayerPlaylist(self, guild: Guild) -> Playlist:
        playerInfo = self.__getRunningPlayerInfo(guild)
        if playerInfo:
            return playerInfo.getPlaylist()

    def getPlayerLock(self, guild: Guild) -> RLock:
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

        voiceChannel = context.author.voice.channel

        playlist = Playlist()
        lock = RLock()
        player = ThreadPlayer(self.__bot, context.guild, context.guild.name,
                              voiceChannel, playlist, lock, guildID, voiceID, self.__receiveCommand, self.__deleteThread)
        playerInfo = ThreadPlayerInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    def __deleteThread(self, guild: Guild) -> None:
        """Tries to delete the thread and removes all the references to it"""
        print(f'[THREAD MANAGER] -> Deleting Thread for guild {guild.name}')
        playerInfo = self.__playersThreads[guild.id]
        if playerInfo:
            thread = playerInfo.getPlayer()
            self.__playersThreads.pop(guild.id)
            del thread

    def __recreateThread(self, guild: Guild, context: Union[Context, Interaction]) -> ThreadPlayerInfo:
        self.__stopPossiblyRunningProcess(guild)

        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id
        voiceChannel = context.author.voice.channel

        playlist = self.__playersThreads[guildID].getPlaylist()
        lock = RLock()
        player = ThreadPlayer(self.__bot, context.guild, context.guild.name,
                              voiceChannel, playlist, lock, guildID, voiceID, self.__receiveCommand, self.__deleteThread)
        playerInfo = ThreadPlayerInfo(player, playlist, lock, context.channel)
        player.start()

        return playerInfo

    async def showNowPlaying(self, guild: Guild, song: Song) -> None:
        processInfo = self.__playersThreads[guild.id]
        playlist = processInfo.getPlaylist()
        txtChannel = processInfo.getTextChannel()

        await ProcessCommandsExecutor.sendNowPlayingToGuild(self.__bot, playlist, txtChannel, song, guild)
