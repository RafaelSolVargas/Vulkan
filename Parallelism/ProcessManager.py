import asyncio
from multiprocessing import Lock, Queue
from multiprocessing.managers import BaseManager, NamespaceProxy
from queue import Empty
from threading import Thread
from typing import Dict, Tuple, Union
from Config.Singleton import Singleton
from discord import Guild, Interaction
from discord.ext.commands import Context
from Parallelism.ProcessExecutor import ProcessCommandsExecutor
from Music.Song import Song
from Parallelism.PlayerProcess import PlayerProcess
from Music.Playlist import Playlist
from Parallelism.ProcessInfo import ProcessInfo, ProcessStatus
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot


class ProcessManager(Singleton):
    """
    Manage all running player process, creating and storing them for future calls
    Deal with the creation of shared memory
    """

    def __init__(self, bot: VulkanBot = None) -> None:
        if not super().created:
            self.__bot = bot
            VManager.register('Playlist', Playlist)
            self.__manager = VManager()
            self.__manager.start()
            self.__playersProcess: Dict[Guild, ProcessInfo] = {}
            self.__playersListeners: Dict[Guild, Tuple[Thread, bool]] = {}
            self.__playersCommandsExecutor: Dict[Guild, ProcessCommandsExecutor] = {}

    def setPlayerInfo(self, guild: Guild, info: ProcessInfo):
        self.__playersProcess[guild.id] = info

    def getOrCreatePlayerInfo(self, guild: Guild, context: Union[Context, Interaction]) -> ProcessInfo:
        """Return the process info for the guild, the user in context must be connected to a voice_channel"""
        try:
            if guild.id not in self.__playersProcess.keys():
                self.__playersProcess[guild.id] = self.__createProcessInfo(guild, context)
            else:
                # If the process has ended create a new one
                if not self.__playersProcess[guild.id].getProcess().is_alive():
                    self.__playersProcess[guild.id] = self.__recreateProcess(guild, context)

            return self.__playersProcess[guild.id]
        except Exception as e:
            print(f'[Error In GetPlayerContext] -> {e}')

    def resetProcess(self, guild: Guild, context: Context) -> None:
        """Restart a running process, already start it to return to play"""
        if guild.id not in self.__playersProcess.keys():
            return None

        # Recreate the process keeping the playlist
        newProcessInfo = self.__recreateProcess(guild, context)
        newProcessInfo.getProcess().start()  # Start the process
        # Send a command to start the play again
        playCommand = VCommands(VCommandsType.PLAY)
        newProcessInfo.getQueueToPlayer().put(playCommand)
        self.__playersProcess[guild.id] = newProcessInfo

    def getRunningPlayerInfo(self, guild: Guild) -> ProcessInfo:
        """Return the process info for the guild, if not, return None"""
        if guild.id not in self.__playersProcess.keys():
            return None

        return self.__playersProcess[guild.id]

    def __createProcessInfo(self, guild: Guild, context: Context) -> ProcessInfo:
        guildID: int = context.guild.id
        textID: int = context.channel.id
        voiceID: int = context.author.voice.channel.id
        authorID: int = context.author.id

        playlist: Playlist = self.__manager.Playlist()
        lock = Lock()
        queueToListen = Queue()
        queueToSend = Queue()
        process = PlayerProcess(context.guild.name, playlist, lock, queueToSend,
                                queueToListen, guildID, textID, voiceID, authorID)
        processInfo = ProcessInfo(process, queueToSend, queueToListen,
                                  playlist, lock, context.channel)

        # Create a Thread to listen for the queue coming from the Player Process, this will redirect the Queue to a async
        thread = Thread(target=self.__listenToCommands,
                        args=(queueToListen, guild), daemon=True)
        self.__playersListeners[guildID] = (thread, False)
        thread.start()

        # Create a Message Controller for this player
        self.__playersCommandsExecutor[guildID] = ProcessCommandsExecutor(self.__bot, guildID)

        return processInfo

    def __recreateProcess(self, guild: Guild, context: Union[Context, Interaction]) -> ProcessInfo:
        """Create a new process info using previous playlist"""
        guildID: int = context.guild.id
        textID: int = context.channel.id
        if isinstance(context, Interaction):
            authorID: int = context.user.id
            voiceID: int = context.user.voice.channel.id
        else:
            authorID: int = context.author.id
            voiceID: int = context.author.voice.channel.id

        playlist: Playlist = self.__playersProcess[guildID].getPlaylist()
        lock = Lock()
        queueToListen = Queue()
        queueToSend = Queue()
        process = PlayerProcess(context.guild.name, playlist, lock, queueToSend,
                                queueToListen, guildID, textID, voiceID, authorID)
        processInfo = ProcessInfo(process, queueToSend, queueToListen,
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

    async def showNowPlaying(self, guildID: int, song: Song) -> None:
        commandExecutor = self.__playersCommandsExecutor[guildID]
        processInfo = self.__playersProcess[guildID]
        await commandExecutor.sendNowPlaying(processInfo, song)


class VManager(BaseManager):
    pass


class VProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
