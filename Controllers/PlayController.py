import asyncio
from Exceptions.Exceptions import DownloadingError, InvalidInput, VulkanError
from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Exceptions.Exceptions import ImpossibleMove, UnknownError
from Controllers.ControllerResponse import ControllerResponse
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Music.Song import Song


class PlayController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__searcher = Searcher()
        self.__down = Downloader()

    async def run(self, args: str) -> ControllerResponse:
        track = " ".join(args)
        requester = self.ctx.author.name

        if track == " ":
            print('Aoba')

        if not self.__user_connected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return ControllerResponse(self.ctx, embed, error)

        if not self.__is_connected():
            success = await self.__connect()
            if not success:
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()
                return ControllerResponse(self.ctx, embed, error)

        try:
            musics = await self.__searcher.search(track)
            if musics is None or len(musics) == 0:
                raise InvalidInput(self.messages.INVALID_INPUT, self.messages.ERROR_TITLE)

            for music in musics:
                song = Song(music, self.player.playlist, requester)
                self.player.playlist.add_song(song)
            quant = len(musics)

            songs_preload = self.player.playlist.songs_to_preload
            await self.__down.preload(songs_preload)

            if quant == 1:
                pos = len(self.player.playlist)
                song = self.__down.finish_one_song(song)
                if song.problematic:
                    embed = self.embeds.SONG_PROBLEMATIC()
                    error = DownloadingError()
                    response = ControllerResponse(self.ctx, embed, error)

                elif not self.player.playing:
                    embed = self.embeds.SONG_ADDED(song.title)
                    response = ControllerResponse(self.ctx, embed)
                else:
                    embed = self.embeds.SONG_ADDED_TWO(song.info, pos)
                    response = ControllerResponse(self.ctx, embed)
            else:
                embed = self.embeds.SONGS_ADDED(quant)
                response = ControllerResponse(self.ctx, embed)

            asyncio.create_task(self.player.play(self.ctx))
            return response

        except Exception as err:
            if isinstance(err, VulkanError):  # If error was already processed
                print(f'DEVELOPER NOTE -> PlayController Error: {err.message}')
                error = err
                embed = self.embeds.CUSTOM_ERROR(error)
            else:
                error = UnknownError()
                embed = self.embeds.UNKNOWN_ERROR()

            return ControllerResponse(self.ctx, embed, error)

    def __user_connected(self) -> bool:
        if self.ctx.author.voice:
            return True
        else:
            return False

    def __is_connected(self) -> bool:
        try:
            voice_channel = self.guild.voice_client.channel

            if not self.guild.voice_client.is_connected():
                return False
            else:
                return True
        except:
            return False

    async def __connect(self) -> bool:
        # if self.guild.voice_client is None:
        try:
            await self.ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            return True
        except:
            return False
