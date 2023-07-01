import asyncio
from time import sleep, time
from urllib.parse import parse_qs, urlparse
from Music.VulkanInitializer import VulkanInitializer
from discord import PCMVolumeTransformer, VoiceClient
from asyncio import AbstractEventLoop, Semaphore, Queue
from multiprocessing import Process, RLock, Lock, Queue
from threading import Thread
from typing import Callable
from discord import Guild, FFmpegPCMAudio, VoiceChannel
from Music.Playlist import Playlist
from Music.Song import Song
from Config.Configs import VConfigs
from Music.VulkanBot import VulkanBot
from Music.Downloader import Downloader
from Parallelism.Commands import VCommands, VCommandsType


class TimeoutClock:
    def __init__(self, callback: Callable, loop: asyncio.AbstractEventLoop):
        self.__callback = callback
        self.__task = loop.create_task(self.__executor())

    async def __executor(self):
        await asyncio.sleep(VConfigs().VC_TIMEOUT)
        await self.__callback()

    def cancel(self):
        self.__task.cancel()


class ProcessPlayer(Process):
    """Process that will play songs, receive commands from the main process by a Queue"""

    def __init__(self, name: str, playlist: Playlist, lock: Lock, queueToReceive: Queue,  queueToSend: Queue, guildID: int, voiceID: int) -> None:
        """
        Start a new process that will have his own bot instance 
        Due to pickle serialization, no objects are stored, the values initialization are being made in the run method
        """
        Process.__init__(self, name=name, group=None, target=None, args=(), kwargs={})
        # Synchronization objects
        self.__playlist: Playlist = playlist
        self.__playlistLock: Lock = lock
        self.__queueReceive: Queue = queueToReceive
        self.__queueSend: Queue = queueToSend
        self.__semStopPlaying: Semaphore = None
        self.__loop: AbstractEventLoop = None
        # Discord context ID
        self.__guildID = guildID
        self.__voiceChannelID = voiceID
        # All information of discord context will be retrieved directly with discord API
        self.__guild: Guild = None
        self.__bot: VulkanBot = None
        self.__voiceChannel: VoiceChannel = None
        self.__voiceClient: VoiceClient = None

        self.__songVolumeUsing = 1
        self.__currentSongChangeVolume = False

        self.__playing = False
        self.__forceStop = False
        self.__botCompletedLoad = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    def run(self) -> None:
        """Method called by process.start(), this will exec the actually _run method in a event loop"""
        try:
            print(f'Starting Player Process for Guild {self.name}')
            self.__playerLock = RLock()
            self.__loop = asyncio.get_event_loop_policy().new_event_loop()
            asyncio.set_event_loop(self.__loop)

            self.__downloader = Downloader()

            self.__semStopPlaying = Semaphore(0)
            self.__loop.run_until_complete(self._run())
        except Exception as e:
            print(f'[ERROR IN PROCESS {self.name}] -> {e}')

    async def _run(self) -> None:
        # Recreate the bot instance and objects using discord API
        self.__bot = await self.__createBotInstance()
        self.__botCompletedLoad = True
        self.__guild = self.__bot.get_guild(self.__guildID)
        self.__voiceChannel = self.__bot.get_channel(self.__voiceChannelID)
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

    def __set_volume(self, volume: float) -> None:
        """Set the volume of the player, must be values between 0 and 100"""
        try:
            if self.__voiceClient is None:
                return
            
            if not isinstance(volume, float):
                print('[PROCESS ERROR] -> Volume instance must be float')
                return

            if volume < 0:
                volume = 0
            if volume > 100:
                volume = 100

            volume = volume / 100

            if not self.__currentSongChangeVolume:
                print('[PROCESS ERROR] -> Cannot change the volume of this song')
                return
            
            self.__songVolumeUsing = volume
            self.__voiceClient.source.volume = volume
        except Exception as e:
            print(e)

    def __verifyIfIsPlaying(self) -> bool:
        if self.__voiceClient is None:
            return False
        if not self.__voiceClient.is_connected():
            return False
        return self.__voiceClient.is_playing() or self.__voiceClient.is_paused()

    async def __playPlaylistSongs(self) -> None:
        """If the player is not running trigger to play a new song"""
        self.__playing = self.__verifyIfIsPlaying()
        if not self.__playing:
            song = None
            with self.__playlistLock:
                with self.__playerLock:
                    song = self.__playlist.next_song()

            if song is not None:
                self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')
                self.__playing = True

    async def __playSong(self, song: Song) -> None:
        """Function that will trigger the player to play the song"""
        try:
            self.__playerLock.acquire()
            if song is None:
                return

            if song.source is None:
                return self.__playNext(None)

            # If not connected, connect to bind channel
            if self.__voiceClient is None:
                await self.__connectToVoiceChannel()

            # If the voice channel disconnect for some reason
            if not self.__voiceClient.is_connected():
                print('[PROCESS PLAYER -> VOICE CHANNEL NOT NULL BUT DISCONNECTED, CONNECTING AGAIN]')
                await self.__connectToVoiceChannel()
            # If the player is connected and playing return the song to the playlist
            elif self.__voiceClient.is_playing():
                print('[PROCESS PLAYER -> SONG ALREADY PLAYING, RETURNING]')
                self.__playlist.add_song_start(song)
                return

            songStillAvailable = self.__verifyIfSongAvailable(song)
            if not songStillAvailable:
                print('[PROCESS PLAYER -> SONG NOT AVAILABLE ANYMORE, DOWNLOADING AGAIN]')
                song = self.__downloadSongAgain(song)

            self.__playing = True
            self.__songPlaying = song

            player = FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
            if not player.is_opus():
                player = PCMVolumeTransformer(player, self.__songVolumeUsing)
                self.__currentSongChangeVolume = True

            self.__voiceClient.play(player, after=lambda e: self.__playNext(e))

            self.__timer.cancel()
            self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)

            nowPlayingCommand = VCommands(VCommandsType.NOW_PLAYING, song)
            self.__queueSend.put(nowPlayingCommand)
        except Exception as e:
            print(f'[PROCESS PLAYER -> ERROR IN PLAY SONG FUNCTION] -> {e}, {type(e)}')
            self.__playNext(None)
        finally:
            self.__playerLock.release()

    def __playNext(self, error) -> None:
        if error is not None:
            print(f'[PROCESS PLAYER -> ERROR PLAYING SONG] -> {error}')
        with self.__playlistLock:
            with self.__playerLock:
                self.__currentSongChangeVolume = False

                if self.__forceStop:  # If it's forced to stop player
                    self.__forceStop = False
                    return None

                song = self.__playlist.next_song()

                if song is not None:
                    self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')
                else:
                    self.__playlist.loop_off()
                    self.__songPlaying = None
                    self.__playing = False
                    # Send a command to the main process put this one to sleep
                    sleepCommand = VCommands(VCommandsType.SLEEPING)
                    self.__queueSend.put(sleepCommand)
                    # Release the semaphore to finish the process
                    self.__semStopPlaying.release()

    def __verifyIfSongAvailable(self, song: Song) -> bool:
        """Verify the song source to see if it's already expired"""
        try:
            parsedUrl = urlparse(song.source)

            if 'expire' not in parsedUrl.query:
                # If already passed 5 hours since the download
                if song.downloadTime + 18000 < int(time()):
                    return False
                return True

            # If the current time plus the song duration plus 10min exceeds the expirationValue
            expireValue = parse_qs(parsedUrl.query)['expire'][0]
            if int(time()) + song.duration + 600 > int(str(expireValue)):
                return False
            return True
        except Exception as e:
            print(f'[PROCESS PLAYER -> ERROR VERIFYING SONG AVAILABILITY] -> {e}')
            return False

    def __downloadSongAgain(self, song: Song) -> Song:
        """Force a download to be executed again, one use case is when the song.source expired and needs to refresh"""
        return self.__downloader.finish_one_song(song)

    async def __playPrev(self, voiceChannelID: int) -> None:
        with self.__playlistLock:
            song = self.__playlist.prev_song()

            with self.__playerLock:
                if song is not None:
                    # If not connect, connect to the user voice channel, may change the channel
                    if self.__voiceClient is None or not self.__voiceClient.is_connected():
                        self.__voiceChannelID = voiceChannelID
                        self.__voiceChannel = self.__guild.get_channel(self.__voiceChannelID)
                        await self.__connectToVoiceChannel()

                    # If already playing, stop the current play
                    if self.__verifyIfIsPlaying():
                        # Will forbidden next_song to execute after stopping current player
                        self.__forceStop = True
                        self.__voiceClient.stop()
                        self.__playing = False

                    self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')

    async def __restartCurrentSong(self) -> None:
        song = self.__playlist.getCurrentSong()
        if song is None:
            song = self.__playlist.next_song()
        if song is None:
            return

        self.__loop.create_task(self.__playSong(song), name=f'Song {song.identifier}')

    def __commandsReceiver(self) -> None:
        # Forces the Thread that listen to the commands to await this bot instance
        # to stablish the connection with discord, may delay when running bots in several servers
        while True:
            if self.__botCompletedLoad:
                break
            sleep(0.1)

        while True:
            command: VCommands = self.__queueReceive.get()
            type = command.getType()
            args = command.getArgs()
            print(f'Player Process {self.__guild.name} received command {type}')

            try:
                self.__playerLock.acquire()
                if type == VCommandsType.PAUSE:
                    self.__pause()
                elif type == VCommandsType.RESUME:
                    asyncio.run_coroutine_threadsafe(self.__resume(), self.__loop)
                elif type == VCommandsType.SKIP:
                    asyncio.run_coroutine_threadsafe(self.__skip(), self.__loop)
                elif type == VCommandsType.PLAY:
                    asyncio.run_coroutine_threadsafe(self.__playPlaylistSongs(), self.__loop)
                elif type == VCommandsType.PREV:
                    asyncio.run_coroutine_threadsafe(self.__playPrev(args), self.__loop)
                elif type == VCommandsType.RESET:
                    asyncio.run_coroutine_threadsafe(self.__reset(), self.__loop)
                elif type == VCommandsType.STOP:
                    asyncio.run_coroutine_threadsafe(self.__stop(), self.__loop)
                elif type == VCommandsType.VOLUME:
                    self.__set_volume(args)
                else:
                    print(f'[PROCESS PLAYER ERROR] -> Unknown Command Received: {command}')
            except Exception as e:
                print(f'[PROCESS PLAYER -> ERROR IN COMMAND RECEIVER] -> {type} - {e}')
            finally:
                self.__playerLock.release()

    def __pause(self) -> None:
        if self.__voiceClient is not None:
            if self.__voiceClient.is_connected():
                if self.__voiceClient.is_playing():
                    self.__voiceClient.pause()

    async def __reset(self) -> None:
        if self.__voiceClient is None:
            return

        if not self.__voiceClient.is_connected():
            await self.__connectToVoiceChannel()
        if self.__songPlaying is not None:
            await self.__restartCurrentSong()

    async def __stop(self) -> None:
        if self.__voiceClient is not None:
            if self.__voiceClient.is_connected():
                with self.__playlistLock:
                    self.__playlist.loop_off()
                    self.__playlist.clear()

                # Send a command to the main process put this to sleep
                sleepCommand = VCommands(VCommandsType.SLEEPING)
                self.__queueSend.put(sleepCommand)
                self.__voiceClient.stop()
                await self.__voiceClient.disconnect()

                self.__songPlaying = None
                self.__playing = False
                self.__voiceClient = None
                self.__semStopPlaying.release()
            # If the voiceClient is not None we finish things
            else:
                await self.__forceBotDisconnectAndStop()

    async def __resume(self) -> None:
        # Lock to work with Player
        with self.__playerLock:
            if self.__voiceClient is not None:
                # If the player is paused then return to play
                if self.__voiceClient.is_paused():
                    return self.__voiceClient.resume()
                # If there is a current song but the voice client is not playing
                elif self.__songPlaying is not None and not self.__voiceClient.is_playing():
                    await self.__playSong(self.__songPlaying)

    async def __skip(self) -> None:
        self.__playing = self.__verifyIfIsPlaying()
        # Lock to work with Player
        with self.__playerLock:
            if self.__playing:
                self.__playing = False
                self.__voiceClient.stop()
            # If for some reason the Bot has disconnect but there is still songs to play
            elif len(self.__playlist.getSongs()) > 0:
                print('[PROCESS PLAYER -> RESTARTING CURRENT SONG]')
                await self.__restartCurrentSong()

    async def __forceBotDisconnectAndStop(self) -> None:
        # Lock to work with Player
        with self.__playerLock:
            if self.__voiceClient is None:
                return
            self.__playing = False
            self.__songPlaying = None
            try:
                self.__voiceClient.stop()
                await self.__voiceClient.disconnect(force=True)
            except Exception as e:
                print(f'[PROCESS PLAYER -> ERROR FORCING BOT TO STOP] -> {e}')
            finally:
                self.__voiceClient = None
            with self.__playlistLock:
                self.__playlist.clear()
                self.__playlist.loop_off()

    async def __createBotInstance(self) -> VulkanBot:
        """Load a new bot instance that should not be directly called."""
        initializer = VulkanInitializer(willListen=False)
        bot = initializer.getBot()

        await bot.startBotCoro(self.__loop)
        await self.__ensureDiscordConnection(bot)
        return bot

    async def __timeoutHandler(self) -> None:
        try:
            # If there is not voiceClient return
            if self.__voiceClient is None:
                return

            # If the bot should not disconnect when alone
            if not VConfigs().SHOULD_AUTO_DISCONNECT_WHEN_ALONE:
                return

            if self.__voiceClient.is_connected():
                if self.__voiceClient.is_playing() or self.__voiceClient.is_paused():
                    if not self.__isBotAloneInChannel():  # If bot is not alone continue to play
                        self.__timer = TimeoutClock(self.__timeoutHandler, self.__loop)
                        return

            # Finish the process
            with self.__playerLock:
                with self.__playlistLock:
                    self.__playlist.loop_off()
                await self.__forceBotDisconnectAndStop()
                # Send command to main process to finish this one
                sleepCommand = VCommands(VCommandsType.SLEEPING)
                self.__queueSend.put(sleepCommand)
                # Release semaphore to finish process
                self.__semStopPlaying.release()
        except Exception as e:
            print(f'[PROCESS PLAYER -> ERROR IN TIMEOUT] -> {e}')

    def __isBotAloneInChannel(self) -> bool:
        try:
            if len(self.__voiceClient.channel.members) <= 1:
                return True
            else:
                return False
        except Exception as e:
            print(f'[PROCESS PLAYER -> ERROR IN CHECK BOT ALONE] -> {e}')
            return False

    async def __ensureDiscordConnection(self, bot: VulkanBot) -> None:
        """Await in this point until connection to discord is established"""
        guild = None
        while guild is None:
            guild = bot.get_guild(self.__guildID)
            await asyncio.sleep(0.2)

    async def __connectToVoiceChannel(self) -> bool:
        try:
            print('[PROCESS PLAYER -> CONNECTING TO VOICE CHANNEL]')
            # If the voiceChannel is not defined yet, like if the Bot is still loading, wait until we get the voiceChannel
            if self.__voiceChannel is None:
                while True:
                    self.__voiceChannel = self.__bot.get_channel(self.__voiceChannelID)
                    if self.__voiceChannel is None:
                        await asyncio.sleep(0.2)
                    else:
                        break

            if self.__voiceClient is not None:
                try:
                    await self.__voiceClient.disconnect(force=True)
                except Exception as e:
                    print(f'[PROCESS PLAYER -> ERROR FORCING DISCONNECT] -> {e}')
            self.__voiceClient = await self.__voiceChannel.connect(reconnect=True, timeout=None)
            return True
        except Exception as e:
            print(f'[PROCESS PLAYER -> ERROR CONNECTING TO VC] -> {e}')
            return False
