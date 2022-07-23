from Config.Exceptions import DownloadingError, InvalidInput, VulkanError
from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import ImpossibleMove, UnknownError
from Handlers.HandlerResponse import HandlerResponse
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Music.Song import Song
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class PlayHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__searcher = Searcher()
        self.__down = Downloader()

    async def run(self, args: str) -> HandlerResponse:
        track = " ".join(args)
        requester = self.ctx.author.name

        if not self.__isUserConnected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)

        try:
            musics = await self.__searcher.search(track)
            if musics is None or len(musics) == 0:
                raise InvalidInput(self.messages.INVALID_INPUT, self.messages.ERROR_TITLE)

            for music in musics:
                song = Song(music, self.player.playlist, requester)
                self.player.playlist.add_song(song)
            quant = len(musics)

            songs_preload = self.player.playlist.getSongsToPreload()
            await self.__down.preload(songs_preload)

            if quant == 1:
                pos = len(self.player.playlist)
                song = self.__down.finish_one_song(song)
                if song.problematic:
                    embed = self.embeds.SONG_PROBLEMATIC()
                    error = DownloadingError()
                    response = HandlerResponse(self.ctx, embed, error)

                elif not self.player.playing:
                    embed = self.embeds.SONG_ADDED(song.title)
                    response = HandlerResponse(self.ctx, embed)
                else:
                    embed = self.embeds.SONG_ADDED_TWO(song.info, pos)
                    response = HandlerResponse(self.ctx, embed)
            else:
                embed = self.embeds.SONGS_ADDED(quant)
                response = HandlerResponse(self.ctx, embed)

            # Get the process context for the current guild
            manager = ProcessManager()
            processContext = manager.getPlayerContext(self.guild, self.ctx)
            # Add the downloaded song to the process playlist
            # All access to shared memory should be protect by acquire the Lock
            with processContext.getLock():
                processContext.getPlaylist().add_song(song)

            # If process already started send a command to the player process by queue
            process = processContext.getProcess()
            queue = processContext.getQueue()
            if process.is_alive():
                command = VCommands(VCommandsType.PLAY)
                queue.put(command)
            else:
                # Start the process
                process.start()

            return response

        except Exception as err:
            if isinstance(err, VulkanError):  # If error was already processed
                print(f'DEVELOPER NOTE -> PlayController Error: {err.message}')
                error = err
                embed = self.embeds.CUSTOM_ERROR(error)
            else:
                print(f'DEVELOPER NOTE -> PlayController Error: {err}')
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()

            return HandlerResponse(self.ctx, embed, error)

    def __isUserConnected(self) -> bool:
        if self.ctx.author.voice:
            return True
        else:
            return False
