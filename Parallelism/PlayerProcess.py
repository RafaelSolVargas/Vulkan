import asyncio
from os import listdir
from discord import Intents, User
from asyncio import AbstractEventLoop, Semaphore
from multiprocessing import Process, Queue
from threading import Lock, Thread
from typing import Callable
from discord import Client, Guild, FFmpegPCMAudio, VoiceChannel, TextChannel
from discord.ext.commands import Context
from Music.Playlist import Playlist
from Music.Song import Song
from Config.Configs import Configs
from discord.ext.commands import Bot
from Parallelism.Commands import VCommands, VCommandsType


class TimeoutClock:
    def __init__(self, callback: Callable, loop: asyncio.AbstractEventLoop):
        self.__callback = callback
        self.__task = loop.create_task(self.__executor())

    async def __executor(self):
        await asyncio.sleep(Configs().VC_TIMEOUT)
        await self.__callback()

    def cancel(self):
        self.__task.cancel()


class PlayerProcess(Process):
    """Process that will play songs, receive commands by a received Queue"""

    def __init__(self, playlist: Playlist, lock: Lock, queue: Queue, guildID: int, textID: int, voiceID: int, authorID: int) -> None:
        """
        Start a new process that will have his own bot instance 
        Due to pickle serialization, no objects are stored, the values initialization are being made in the run method
        """
        Process.__init__(self, group=None, target=None, args=(), kwargs={})
        # Synchronization objects
        self.__playlist: Playlist = playlist
        self.__lock: Lock = lock
        self.__queue: Queue = queue
        self.__semStopPlaying: Semaphore = None
        self.__loop: AbstractEventLoop = None
        # Discord context ID
        self.__textChannelID = textID
        self.__guildID = guildID
        self.__voiceChannelID = voiceID
        self.__authorID = authorID
        # All information of discord context will be retrieved directly with discord API
        self.__guild: Guild = None
        self.__bot: Client = None
        self.__voiceChannel: VoiceChannel = None
        self.__textChannel: TextChannel = None
        self.__author: User = None

        self.__configs: Configs = None
        self.__playing = False
        self.__forceStop = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    def run(self) -> None:
        """Method called by process.start(), this will exec the actually _run method in a event loop"""
        self.__loop = asyncio.get_event_loop()
        self.__configs = Configs()

        self.__semStopPlaying = Semaphore(0)
        self.__stopped = asyncio.Event()
        self.__loop.run_until_complete(self._run())

    async def _run(self) -> None:
        # Recreate the bot instance and objects using discord API
        self.__bot = await self.__createBotInstance()
        self.__guild = self.__bot.get_guild(self.__guildID)
        self.__voiceChannel = self.__bot.get_channel(self.__voiceChannelID)
        self.__textChannel = self.__bot.get_channel(self.__textChannelID)
        self.__author = self.__bot.get_channel(self.__authorID)
        # Connect to voice Channel
        await self.__connectToVoiceChannel()

        # Start the timeout function
        self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)
        # Thread that will receive commands to be executed in this Process
        self.__commandsReceiver = Thread(target=self.__commandsReceiver, daemon=True)
        self.__commandsReceiver.start()

        # Start a Task to play songs
        self.__loop.create_task(self.__playPlaylistSongs())
        # Try to acquire a semaphore, it'll be release when timeout function trigger, we use the Semaphore
        # from the asyncio lib to not block the event loop
        await self.__semStopPlaying.acquire()

    async def __playPlaylistSongs(self) -> None:
        print(f'Playing: {self.__playing}')
        if not self.__playing:
            with self.__lock:
                print('Next Song Aqui')
                song = self.__playlist.next_song()

            await self.__playSong(song)

    async def __playSong(self, song: Song) -> None:
        try:
            source = await self.__ensureSource(song)
            if source is None:
                self.__playNext(None)
            self.__playing = True

            player = FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
            voice = self.__guild.voice_client
            voice.play(player, after=lambda e: self.__playNext(e))

            self.__timer.cancel()
            self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)

            # await self.__context.invoke(self.__bot.get_command('np'))
        except Exception as e:
            print(f'[ERROR IN PLAY SONG] -> {e}')
            self.__playNext(None)

    def __playNext(self, error) -> None:
        if self.__forceStop:  # If it's forced to stop player
            self.__forceStop = False
            return None

        with self.__lock:
            song = self.__playlist.next_song()

        if song is not None:
            coro = self.__playSong(song)
            self.__bot.loop.create_task(coro)
        else:
            self.__playing = False

    def __commandsReceiver(self) -> None:
        while True:
            command: VCommands = self.__queue.get()
            type = command.getType()
            args = command.getArgs()

            print(f'Command Received: {type}')
            if type == VCommandsType.PAUSE:
                self.pause()
            elif type == VCommandsType.PLAY:
                self.__loop.create_task(self.__playPlaylistSongs())
            elif type == VCommandsType.PLAY_PREV:
                self.__playPrev()
            elif type == VCommandsType.RESUME:
                pass
            elif type == VCommandsType.SKIP:
                pass
            else:
                print(f'[ERROR] -> Unknown Command Received: {command}')

    def pause(self):
        print(id(self))

    async def __playPrev(self, ctx: Context) -> None:
        with self.__lock:
            song = self.__playlist.prev_song()
        if song is not None:
            if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
                # Will forbidden next_song to execute after stopping current player
                self.__forceStop = True
                self.__guild.voice_client.stop()
                self.__playing = False

            await self.__playSong(ctx, song)

    async def __forceStop(self) -> None:
        try:
            if self.__guild.voice_client is None:
                return

            self.__guild.voice_client.stop()
            await self.__guild.voice_client.disconnect()
            with self.__lock:
                self.__playlist.clear()
                self.__playlist.loop_off()
        except Exception as e:
            print(f'DEVELOPER NOTE -> Force Stop Error: {e}')

    async def __createBotInstance(self) -> Client:
        """Load a new bot instance that should not be directly called.
        Get the guild, voice and text Channel in discord API using IDs passed in constructor
        """
        intents = Intents.default()
        intents.members = True
        bot = Bot(command_prefix='Rafael',
                  pm_help=True,
                  case_insensitive=True,
                  intents=intents)
        bot.remove_command('help')

        # Add the Cogs for this bot too
        for filename in listdir(f'./{self.__configs.COMMANDS_PATH}'):
            if filename.endswith('.py'):
                bot.load_extension(f'{self.__configs.COMMANDS_PATH}.{filename[:-3]}')

        # Login and connect the bot instance to discord API
        task = self.__loop.create_task(bot.login(token=self.__configs.BOT_TOKEN, bot=True))
        await task
        self.__loop.create_task(bot.connect(reconnect=True))
        # Sleep to wait connection to be established
        await asyncio.sleep(2)

        return bot

    async def __timeoutHandler(self) -> None:
        if self.__guild.voice_client is None:
            return

        if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
            self.__timer = TimeoutClock(self.__timeoutHandler)

        elif self.__guild.voice_client.is_connected():
            with self.__lock:
                self.__playlist.clear()
                self.__playlist.loop_off()
            await self.__guild.voice_client.disconnect()
            # Release semaphore to finish process
            self.__semStopPlaying.release()

    async def __ensureSource(self, song: Song) -> str:
        while True:
            if song.source is not None:  # If song got downloaded
                return song.source

            if song.problematic:  # If song got any error
                return None

            await asyncio.sleep(0.1)

    def __is_connected(self) -> bool:
        try:
            if not self.__voiceChannel.is_connected():
                return False
            else:
                return True
        except:
            return False

    async def __connectToVoiceChannel(self) -> bool:
        try:
            await self.__voiceChannel.connect(reconnect=True, timeout=None)
            return True
        except:
            return False
