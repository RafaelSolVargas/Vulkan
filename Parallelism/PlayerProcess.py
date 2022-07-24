import asyncio
from os import listdir
from discord import Intents, User, Member
from asyncio import AbstractEventLoop, Semaphore
from multiprocessing import Process, Queue, RLock
from threading import Lock, Thread
from typing import Callable, List
from discord import Client, Guild, FFmpegPCMAudio, VoiceChannel, TextChannel
from Music.Playlist import Playlist
from Music.Song import Song
from Config.Configs import Configs
from Config.Messages import Messages
from discord.ext.commands import Bot
from Views.Embeds import Embeds
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
    """Process that will play songs, receive commands from the main process by a Queue"""

    def __init__(self, name: str, playlist: Playlist, lock: Lock, queue: Queue, guildID: int, textID: int, voiceID: int, authorID: int) -> None:
        """
        Start a new process that will have his own bot instance 
        Due to pickle serialization, no objects are stored, the values initialization are being made in the run method
        """
        Process.__init__(self, name=name, group=None, target=None, args=(), kwargs={})
        # Synchronization objects
        self.__playlist: Playlist = playlist
        self.__playlistLock: Lock = lock
        self.__playerLock: RLock = None
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
        self.__botMember: Member = None

        self.__configs: Configs = None
        self.__embeds: Embeds = None
        self.__messages: Messages = None
        self.__playing = False
        self.__forceStop = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    def run(self) -> None:
        """Method called by process.start(), this will exec the actually _run method in a event loop"""
        try:
            print(f'Starting Process {self.name}')
            self.__playerLock = RLock()
            self.__loop = asyncio.get_event_loop()

            self.__configs = Configs()
            self.__messages = Messages()
            self.__embeds = Embeds()

            self.__semStopPlaying = Semaphore(0)
            self.__loop.run_until_complete(self._run())
        except Exception as e:
            print(f'[Error in Process {self.name}] -> {e}')

    async def _run(self) -> None:
        # Recreate the bot instance and objects using discord API
        self.__bot = await self.__createBotInstance()
        self.__guild = self.__bot.get_guild(self.__guildID)
        self.__voiceChannel = self.__bot.get_channel(self.__voiceChannelID)
        self.__textChannel = self.__bot.get_channel(self.__textChannelID)
        self.__author = self.__bot.get_channel(self.__authorID)
        self.__botMember = self.__getBotMember()
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
        # In this point the process should finalize
        self.__timer.cancel()

    async def __playPlaylistSongs(self) -> None:
        if not self.__playing:
            with self.__playlistLock:
                song = self.__playlist.next_song()

            if song is not None:
                self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')

    async def __playSong(self, song: Song) -> None:
        """Function that will trigger the player to play the song"""
        try:
            if song is None:
                return

            if song.source is None:
                return self.__playNext(None)

            # If not connected, connect to bind channel
            if self.__guild.voice_client is None:
                self.__connectToVoiceChannel()

            # If the player is already playing return
            if self.__guild.voice_client.is_playing():
                return

            self.__playing = True

            player = FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
            self.__guild.voice_client.play(player, after=lambda e: self.__playNext(e))

            self.__timer.cancel()
            self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)

            await self.__showNowPlaying()
        except Exception as e:
            print(f'[ERROR IN PLAY SONG] -> {e}, {type(e)}')
            self.__playNext(None)

    def __playNext(self, error) -> None:
        with self.__playerLock:
            if self.__forceStop:  # If it's forced to stop player
                self.__forceStop = False
                return None

            with self.__playlistLock:
                song = self.__playlist.next_song()

            if song is not None:
                self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')
            else:
                with self.__playlistLock:
                    self.__playlist.loop_off()

                self.__playing = False

    async def __playPrev(self, voiceChannelID: int) -> None:
        with self.__playlistLock:
            song = self.__playlist.prev_song()

        if song is not None:
            if self.__guild.voice_client is None:  # If not connect, connect to the user voice channel
                self.__voiceChannelID = voiceChannelID
                self.__voiceChannel = self.__guild.get_channel(self.__voiceChannelID)
                self.__connectToVoiceChannel()

            # If already playing, stop the current play
            if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
                # Will forbidden next_song to execute after stopping current player
                self.__forceStop = True
                self.__guild.voice_client.stop()
                self.__playing = False

            self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')

    def __commandsReceiver(self) -> None:
        while True:
            command: VCommands = self.__queue.get()
            type = command.getType()
            args = command.getArgs()

            try:
                self.__playerLock.acquire()
                if type == VCommandsType.PAUSE:
                    self.__pause()
                elif type == VCommandsType.RESUME:
                    self.__resume()
                elif type == VCommandsType.SKIP:
                    self.__skip()
                elif type == VCommandsType.PLAY:
                    asyncio.run_coroutine_threadsafe(self.__playPlaylistSongs(), self.__loop)
                elif type == VCommandsType.PREV:
                    asyncio.run_coroutine_threadsafe(self.__playPrev(args), self.__loop)
                elif type == VCommandsType.RESET:
                    asyncio.run_coroutine_threadsafe(self.__reset(), self.__loop)
                elif type == VCommandsType.STOP:
                    asyncio.run_coroutine_threadsafe(self.__stop(), self.__loop)
                else:
                    print(f'[ERROR] -> Unknown Command Received: {command}')
            except Exception as e:
                print(f'[ERROR IN COMMAND RECEIVER] -> {type} - {e}')
            finally:
                self.__playerLock.release()

    def __pause(self) -> None:
        if self.__guild.voice_client is not None:
            if self.__guild.voice_client.is_playing():
                self.__guild.voice_client.pause()

    async def __reset(self) -> None:
        if self.__guild.voice_client is None:
            return
        # Reset the bot
        self.__guild.voice_client.stop()
        await self.__guild.voice_client.disconnect()
        self.__playlist.clear()
        self.__playlist.loop_off()
        await self.__botMember.move_to(None)
        # Release semaphore to finish the current player process
        self.__semStopPlaying.release()

    async def __stop(self) -> None:
        if self.__guild.voice_client is not None:
            if self.__guild.voice_client.is_connected():
                with self.__playlistLock:
                    self.__playlist.clear()
                    self.__playlist.loop_off()
                    self.__guild.voice_client.stop()
                    await self.__guild.voice_client.disconnect()

    def __resume(self) -> None:
        if self.__guild.voice_client is not None:
            if self.__guild.voice_client.is_paused():
                self.__guild.voice_client.resume()

    def __skip(self) -> None:
        if self.__guild.voice_client is not None:
            self.__guild.voice_client.stop()

    async def __forceStop(self) -> None:
        if self.__guild.voice_client is None:
            return

        self.__guild.voice_client.stop()
        await self.__guild.voice_client.disconnect()
        with self.__playlistLock:
            self.__playlist.clear()
            self.__playlist.loop_off()

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
        await self.__ensureDiscordConnection(bot)

        return bot

    async def __timeoutHandler(self) -> None:
        try:
            print('TimeoutHandler')
            if self.__guild.voice_client is None:
                return

            if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
                self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)

            elif self.__guild.voice_client.is_connected():
                self.__playerLock.acquire()
                with self.__playlistLock:
                    self.__playlist.clear()
                    self.__playlist.loop_off()
                self.__playing = False
                await self.__guild.voice_client.disconnect()
                # Release semaphore to finish process
                self.__playerLock.release()
                self.__semStopPlaying.release()
        except Exception as e:
            print(f'[Error in Timeout] -> {e}')

    def __is_connected(self) -> bool:
        try:
            if not self.__voiceChannel.is_connected():
                return False
            else:
                return True
        except:
            return False

    async def __ensureDiscordConnection(self, bot: Client) -> None:
        """Await in this point until connection to discord is established"""
        guild = None
        while guild is None:
            guild = bot.get_guild(self.__guildID)
            await asyncio.sleep(0.2)

    async def __connectToVoiceChannel(self) -> bool:
        try:
            await self.__voiceChannel.connect(reconnect=True, timeout=None)
            return True
        except Exception as e:
            print(f'[ERROR CONNECTING TO VC] -> {e}')
            return False

    def __getBotMember(self) -> Member:
        guild_members: List[Member] = self.__guild.members
        for member in guild_members:
            if member.id == self.__bot.user.id:
                return member

    async def __showNowPlaying(self) -> None:
        # Get the current process of the guild
        with self.__playlistLock:
            if not self.__playing or self.__playlist.getCurrentSong() is None:
                embed = self.__embeds.NOT_PLAYING()
                await self.__textChannel.send(embed=embed)
                return

            if self.__playlist.isLoopingOne():
                title = self.__messages.ONE_SONG_LOOPING
            else:
                title = self.__messages.SONG_PLAYING

            info = self.__playlist.getCurrentSong().info
            embed = self.__embeds.SONG_INFO(info, title)
            await self.__textChannel.send(embed=embed)
