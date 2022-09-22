import asyncio
from typing import List
from Config.Exceptions import DownloadingError, InvalidInput, VulkanError
from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import ImpossibleMove, UnknownError
from Handlers.HandlerResponse import HandlerResponse
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Music.Song import Song
from Parallelism.ProcessInfo import ProcessInfo
from Parallelism.Commands import VCommands, VCommandsType
from Music.VulkanBot import VulkanBot
from typing import Union
from discord import Interaction


class PlayHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)
        self.__searcher = Searcher()
        self.__down = Downloader()

    async def run(self, track: str) -> HandlerResponse:
        requester = self.ctx.author.name

        if not self.__isUserConnected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)

        try:
            # Search for musics and get the name of each song
            musicsInfo = await self.__searcher.search(track)
            if musicsInfo is None or len(musicsInfo) == 0:
                raise InvalidInput(self.messages.INVALID_INPUT, self.messages.ERROR_TITLE)

            # Get the process context for the current guild
            processManager = self.config.getProcessManager()
            processInfo = processManager.getOrCreatePlayerInfo(self.guild, self.ctx)
            playlist = processInfo.getPlaylist()
            process = processInfo.getProcess()
            if not process.is_alive():  # If process has not yet started, start
                process.start()

            # Create the Songs objects
            songs: List[Song] = []
            for musicInfo in musicsInfo:
                songs.append(Song(musicInfo, playlist, requester))

            if len(songs) == 1:
                # If only one music, download it directly
                song = self.__down.finish_one_song(songs[0])
                if song.problematic:  # If error in download song return
                    embed = self.embeds.SONG_PROBLEMATIC()
                    error = DownloadingError()
                    return HandlerResponse(self.ctx, embed, error)

                # If not playing
                if not playlist.getCurrentSong():
                    embed = self.embeds.SONG_ADDED(song.title)
                    response = HandlerResponse(self.ctx, embed)
                else:  # If already playing
                    pos = len(playlist.getSongs())
                    embed = self.embeds.SONG_ADDED_TWO(song.info, pos)
                    response = HandlerResponse(self.ctx, embed)

                # Add the unique song to the playlist and send a command to player process
                processLock = processInfo.getLock()
                acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
                if acquired:
                    playlist.add_song(song)
                    # Release the acquired Lock
                    processLock.release()
                    queue = processInfo.getQueueToPlayer()
                    playCommand = VCommands(VCommandsType.PLAY, None)
                    queue.put(playCommand)
                else:
                    processManager.resetProcess(self.guild, self.ctx)
                    embed = self.embeds.PLAYER_RESTARTED()
                    return HandlerResponse(self.ctx, embed)

                return response
            else:  # If multiple songs added
                # Trigger a task to download all songs and then store them in the process playlist
                asyncio.create_task(self.__downloadSongsAndStore(songs, processInfo))

                embed = self.embeds.SONGS_ADDED(len(songs))
                return HandlerResponse(self.ctx, embed)

        except DownloadingError as error:
            embed = self.embeds.DOWNLOADING_ERROR()
            return HandlerResponse(self.ctx, embed, error)
        except Exception as error:
            if isinstance(error, VulkanError):  # If error was already processed
                print(f'DEVELOPER NOTE -s> PlayController Error: {error.message}', {type(error)})
                embed = self.embeds.CUSTOM_ERROR(error)
            else:
                print(f'DEVELOPER NOTE -> PlayController Error: {error}, {type(error)}')
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()

            return HandlerResponse(self.ctx, embed, error)

    async def __downloadSongsAndStore(self, songs: List[Song], processInfo: ProcessInfo) -> None:
        playlist = processInfo.getPlaylist()
        queue = processInfo.getQueueToPlayer()
        playCommand = VCommands(VCommandsType.PLAY, None)
        # Trigger a task for each song to be downloaded
        tasks: List[asyncio.Task] = []
        for song in songs:
            task = asyncio.create_task(self.__down.download_song(song))
            tasks.append(task)

        # In the original order, await for the task and then if successfully downloaded add in the playlist
        processManager = self.config.getProcessManager()
        for index, task in enumerate(tasks):
            await task
            song = songs[index]
            if not song.problematic:  # If downloaded add to the playlist and send play command
                processInfo = processManager.getOrCreatePlayerInfo(self.guild, self.ctx)
                processLock = processInfo.getLock()
                acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
                if acquired:
                    playlist.add_song(song)
                    queue.put(playCommand)
                    processLock.release()
                else:
                    processManager.resetProcess(self.guild, self.ctx)

    def __isUserConnected(self) -> bool:
        if self.ctx.author.voice:
            return True
        else:
            return False
