import asyncio
from discord.ext import commands
from discord import Client, Guild, FFmpegPCMAudio
from discord.ext.commands import Context
from Music.Downloader import Downloader
from Music.Playlist import Playlist
from Music.Song import Song
from Utils.Utils import Timer


class Player(commands.Cog):
    def __init__(self, bot: Client, guild: Guild):
        self.__down: Downloader = Downloader()
        self.__playlist: Playlist = Playlist()
        self.__bot: Client = bot
        self.__guild: Guild = guild

        self.__timer = Timer(self.__timeout_handler)
        self.__playing = False

        # Flag to control if the player should stop totally the playing
        self.__force_stop = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    @property
    def playing(self) -> bool:
        return self.__playing

    @property
    def playlist(self) -> Playlist:
        return self.__playlist

    async def play(self, ctx: Context) -> str:
        if not self.__playing:
            first_song = self.__playlist.next_song()
            await self.__play_music(ctx, first_song)

    async def play_prev(self, ctx: Context) -> None:
        song = self.__playlist.prev_song()
        if song is not None:
            if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
                # Will forbidden next_song to execute after stopping current player
                self.__force_stop = True
                self.__guild.voice_client.stop()
                self.__playing = False

            await self.__play_music(ctx, song)

    async def force_stop(self) -> None:
        try:
            if self.__guild.voice_client is None:
                return

            self.__guild.voice_client.stop()
            await self.__guild.voice_client.disconnect()
            self.__playlist.clear()
            self.__playlist.loop_off()
        except Exception as e:
            print(f'DEVELOPER NOTE -> Force Stop Error: {e}')

    def __play_next(self, error, ctx: Context) -> None:
        if self.__force_stop:  # If it's forced to stop player
            self.__force_stop = False
            return None

        song = self.__playlist.next_song()

        if song is not None:
            coro = self.__play_music(ctx, song)
            self.__bot.loop.create_task(coro)
        else:
            self.__playing = False

    async def __play_music(self, ctx: Context, song: Song) -> None:
        try:
            source = await self.__ensure_source(song)
            if source is None:
                self.__play_next(None, ctx)

            self.__playing = True

            player = FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
            voice = self.__guild.voice_client
            voice.play(player, after=lambda e: self.__play_next(e, ctx))

            self.__timer.cancel()
            self.__timer = Timer(self.__timeout_handler)

            await ctx.invoke(self.__bot.get_command('np'))

            songs = self.__playlist.songs_to_preload
            asyncio.create_task(self.__down.preload(songs))
        except:
            self.__play_next(None, ctx)

    async def __timeout_handler(self) -> None:
        if self.__guild.voice_client is None:
            return

        if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
            self.__timer = Timer(self.__timeout_handler)

        elif self.__guild.voice_client.is_connected():
            self.__playlist.clear()
            self.__playlist.loop_off()
            await self.__guild.voice_client.disconnect()

    async def __ensure_source(self, song: Song) -> str:
        while True:
            await asyncio.sleep(0.1)
            if song.source is not None:  # If song got downloaded
                return song.source

            if song.problematic:  # If song got any error
                return None
