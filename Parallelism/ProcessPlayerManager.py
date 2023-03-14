import asyncio
from enum import Enum
from multiprocessing import Lock, Process, Queue
from multiprocessing.managers import BaseManager, NamespaceProxy
from queue import Empty
from threading import Thread
from typing import Dict, Tuple, Union
from Config.Singleton import Singleton
from discord import Guild, Interaction, TextChannel, VoiceChannel
from discord.ext.commands import Context
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Parallelism.ProcessExecutor import ProcessCommandsExecutor
from Music.Song import Song
from Parallelism.ProcessPlayer import ProcessPlayer
from Music.Playlist import Playlist
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot


class ProcessStatus(Enum):
    RUNNING = 'Running'
    SLEEPING = 'Sleeping'


class PlayerProcessInfo:
    """
    Class to store the reference to all structures to maintain a process player
    """

    def __init__(self, process: Process, queueToPlayer: Queue, queueToMain: Queue, playlist: Playlist, lock: Lock, textChannel: TextChannel) -> None:
        self.__process = process
        self.__queueToPlayer = queueToPlayer
        self.__queueToMain = queueToMain
        self.__playlist = playlist
        self.__lock = lock
        self.__textChannel = textChannel
        self.__status = ProcessStatus.RUNNING

    def setProcess(self, newProcess: Process) -> None:
        self.__process = newProcess

    def getStatus(self) -> ProcessStatus:
        return self.__status

    def setStatus(self, status: ProcessStatus) -> None:
        self.__status = status

    def getProcess(self) -> Process:
        return self.__process

    def getQueueToPlayer(self) -> Queue:
        return self.__queueToPlayer

    def getQueueToMain(self) -> Queue:
        return self.__queueToMain

    def getPlaylist(self) -> Playlist:
        return self.__playlist

    def getLock(self) -> Lock:
        return self.__lock

    def getTextChannel(self) -> TextChannel:
        return self.__textChannel


class ProcessPlayerManager(Singleton, AbstractPlayersManager):
    """
    Manage all running player process, creating and storing them for future calls
    Deals with the creation of shared memory
    """

    def __init__(self, bot: VulkanBot = None) -> None:
        if not super().created:
            self.__bot = bot
            VManager.register('Playlist', Playlist)
            VManager.register('VoiceChannel', VoiceChannel)
            self.__manager = VManager()
            self.__manager.start()
            self.__playersProcess: Dict[int, PlayerProcessInfo] = {}
            self.__playersListeners: Dict[int, Tuple[Thread, bool]] = {}
            self.__playersCommandsExecutor: Dict[int, ProcessCommandsExecutor] = {}

    async def sendCommandToPlayer(self, command: VCommands, guild: Guild, context: Union[Context, Interaction], forceCreation: bool = False):
        if forceCreation:
            processInfo = self.createPlayerForGuild(guild, context)
        else:
            processInfo = self.__getRunningPlayerInfo(guild)
        if processInfo == None:
            return

        if processInfo.getStatus() == ProcessStatus.SLEEPING:
            self.resetPlayer(guild, context)
            processInfo = self.__getRunningPlayerInfo(guild)

        queue = processInfo.getQueueToPlayer()
        self.__putCommandInQueue(queue, command)

    def getPlayerPlaylist(self, guild: Guild) -> Playlist:
        playerInfo = self.__getRunningPlayerInfo(guild)
        if playerInfo:
            return playerInfo.getPlaylist()

    def getPlayerLock(self, guild: Guild) -> Lock:
        playerInfo = self.__getRunningPlayerInfo(guild)
        if playerInfo:
            return playerInfo.getLock()

    def verifyIfPlayerExists(self, guild: Guild) -> bool:
        return guild.id in self.__playersProcess.keys()

    def createPlayerForGuild(self, guild: Guild, context: Union[Context, Interaction]) -> None:
        try:
            if guild.id not in self.__playersProcess.keys():
                self.__playersProcess[guild.id] = self.__createProcessPlayerInfo(guild, context)
            else:
                # If the process has ended create a new one
                if not self.__playersProcess[guild.id].getProcess().is_alive():
                    self.__playersProcess[guild.id] = self.__recreateProcess(guild, context)

            # Start the process
            self.__playersProcess[guild.id].getProcess().start()
            return self.__playersProcess[guild.id]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def resetPlayer(self, guild: Guild, context: Context) -> None:
        """Restart a running process, already start it to return to play"""
        if guild.id not in self.__playersProcess.keys():
            return None

        # Recreate the process keeping the playlist
        newProcessInfo = self.__recreateProcess(guild, context)
        newProcessInfo.getProcess().start()  # Start the process
        # Send a command to start the play again
        playCommand = VCommands(VCommandsType.PLAY)
        self.__putCommandInQueue(newProcessInfo.getQueueToPlayer(), playCommand)
        self.__playersProcess[guild.id] = newProcessInfo

    def __getRunningPlayerInfo(self, guild: Guild) -> PlayerProcessInfo:
        """Return the process info for the guild, if not, return None"""
        if guild.id not in self.__playersProcess.keys():
            print('Process Info not found')
            return None

        return self.__playersProcess[guild.id]

    def __createProcessPlayerInfo(self, guild: Guild, context: Context) -> PlayerProcessInfo:
        guildID: int = context.guild.id
        voiceID: int = context.author.voice.channel.id

        playlist: Playlist = self.__manager.Playlist()
        lock = Lock()
        queueToListen = Queue()
        queueToSend = Queue()
        process = ProcessPlayer(context.guild.name, playlist, lock, queueToSend,
                                queueToListen, guildID, voiceID)
        processInfo = PlayerProcessInfo(process, queueToSend, queueToListen,
                                        playlist, lock, context.channel)

        # Create a Thread to listen for the queue coming from the Player Process, this will redirect the Queue to a async
        thread = Thread(target=self.__listenToCommands,
                        args=(queueToListen, guild), daemon=True)
        self.__playersListeners[guildID] = (thread, False)
        thread.start()

        # Create a Message Controller for this player
        self.__playersCommandsExecutor[guildID] = ProcessCommandsExecutor(self.__bot, guildID)

        return processInfo

    def __stopPossiblyRunningProcess(self, guild: Guild):
        try:
            if guild.id in self.__playersProcess.keys():
                playerProcess = self.__playersProcess[guild.id]
                process = playerProcess.getProcess()
                process.close()
                process.kill()
        except ValueError:
            pass
        except Exception as e:
            print(f'[WARNINGS] -> {e}')

    def __recreateProcess(self, guild: Guild, context: Union[Context, Interaction]) -> PlayerProcessInfo:
        """Create a new process info using previous playlist"""
        self.__stopPossiblyRunningProcess(guild)

        guildID: int = context.guild.id
        if isinstance(context, Interaction):
            voiceID: int = context.user.voice.channel.id
        else:
            voiceID: int = context.author.voice.channel.id

        playlist: Playlist = self.__playersProcess[guildID].getPlaylist()
        lock = Lock()
        queueToListen = Queue()
        queueToSend = Queue()
        process = ProcessPlayer(context.guild.name, playlist, lock, queueToSend,
                                queueToListen, guildID, voiceID)
        processInfo = PlayerProcessInfo(process, queueToSend, queueToListen,
                                        playlist, lock, context.channel)

        # Create a Thread to listen for the queue coming from the Player Process, this will redirect the Queue to a async
        thread = Thread(target=self.__listenToCommands,
                        args=(queueToListen, guild), daemon=True)
        self.__playersListeners[guildID] = (thread, False)
        thread.start()

        return processInfo

    def __listenToCommands(self, queue: Queue, guild: Guild) -> None:
        guildID = guild.id
        while True:
            shouldEnd = self.__playersListeners[guildID][1]
            if shouldEnd:
                break

            try:
                command: VCommands = queue.get(timeout=5)
                commandType = command.getType()
                args = command.getArgs()

                print(f'Process {guild.name} sended command {commandType}')
                if commandType == VCommandsType.NOW_PLAYING:
                    asyncio.run_coroutine_threadsafe(self.showNowPlaying(
                        guild.id, args), self.__bot.loop)
                elif commandType == VCommandsType.TERMINATE:
                    # Delete the process elements and return, to finish task
                    self.__terminateProcess(guildID)
                    return
                elif commandType == VCommandsType.SLEEPING:
                    # The process might be used again
                    self.__sleepingProcess(guildID)
                    return
                else:
                    print(f'[ERROR] -> Unknown Command Received from Process: {commandType}')
            except Empty:
                continue
            except Exception as e:
                print(f'[ERROR IN LISTENING PROCESS] -> {guild.name} - {e}')

    def __terminateProcess(self, guildID: int) -> None:
        # Delete all structures associated with the Player
        del self.__playersProcess[guildID]
        del self.__playersCommandsExecutor[guildID]
        threadListening = self.__playersListeners[guildID]
        threadListening._stop()
        del self.__playersListeners[guildID]

    def __sleepingProcess(self, guildID: int) -> None:
        # Disable all process structures, except Playlist
        queue1 = self.__playersProcess[guildID].getQueueToMain()
        queue2 = self.__playersProcess[guildID].getQueueToPlayer()
        queue1.close()
        queue1.join_thread()
        queue2.close()
        queue2.join_thread()
        # Set the status of this process as sleeping, only the playlist object remains
        self.__playersProcess[guildID].setStatus(ProcessStatus.SLEEPING)

    def __putCommandInQueue(self, queue: Queue, command: VCommands) -> None:
        try:
            queue.put(command)
        except Exception as e:
            print(f'[ERROR PUTTING COMMAND IN QUEUE] -> {e}')

    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        commandExecutor = self.__playersCommandsExecutor[guildID]
        processInfo = self.__playersProcess[guildID]
        playlist = processInfo.getPlaylist()
        channel = processInfo.getTextChannel()
        await commandExecutor.sendNowPlaying(playlist, channel, song)


class VManager(BaseManager):
    pass


class VProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
