from discord.ext import commands
from Config.Config import Configs
from discord import Client, Guild, FFmpegPCMAudio, Embed
from discord.ext.commands import Context
from datetime import timedelta
from Music.Downloader import Downloader
from Music.Playlist import Playlist
from Music.Searcher import Searcher
from Music.Song import Song
from Music.Types import Provider
from Utils.Utils import *


class Player(commands.Cog):
    def __init__(self, bot: Client, guild: Guild):
        self.__searcher: Searcher = Searcher()
        self.__down: Downloader = Downloader()
        self.__playlist: Playlist = Playlist()
        self.__bot: Client = bot
        self.__guild: Guild = guild

        self.__timer = Timer(self.__timeout_handler)
        self.__playing = False
        self.__config = Configs()

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
        if self.__playlist.looping_one or self.__playlist.looping_all:  # Do not allow play if loop
            embed = Embed(
                title=self.__config.SONG_PLAYER,
                description=self.__config.LOOP_ON,
                colour=self.__config.COLOURS['blue']
            )
            await ctx.send(embed=embed)
            return None

        song = self.__playlist.prev_song()  # Prepare the prev song to play again
        if song == None:
            embed = Embed(
                title=self.__config.SONG_PLAYER,
                description=self.__config.NOT_PREVIOUS,
                colour=self.__config.COLOURS['blue']
            )
            await ctx.send(embed=embed)
        else:
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

        if song != None:
            coro = self.__play_music(ctx, song)
            self.__bot.loop.create_task(coro)
        else:
            self.__playing = False

    async def __play_music(self, ctx: Context, song: Song) -> None:
        try:
            source = self.__ensure_source(song)
            if source == None:
                self.__play_next(None, ctx)

            self.__playing = True

            player = FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
            self.__guild.voice_client.play(
                player, after=lambda e: self.__play_next(e, ctx))

            self.__timer.cancel()
            self.__timer = Timer(self.__timeout_handler)

            await ctx.invoke(self.__bot.get_command('np'))

            songs = self.__playlist.songs_to_preload
            await self.__down.preload(songs)
        except:
            self.__play_next(None, ctx)

    def __format_embed(self, info: dict, title='', position='Playing Now') -> Embed:
        embedvc = Embed(
            title=title,
            description=f"[{info['title']}]({info['original_url']})",
            color=self.__config.COLOURS['blue']
        )

        embedvc.add_field(name=self.__config.SONGINFO_UPLOADER,
                          value=info['uploader'],
                          inline=False)

        embedvc.add_field(name=self.__config.SONGINFO_REQUESTER,
                          value=info['requester'],
                          inline=True)

        if 'thumbnail' in info.keys():
            embedvc.set_thumbnail(url=info['thumbnail'])

        if 'duration' in info.keys():
            duration = str(timedelta(seconds=info['duration']))
            embedvc.add_field(name=self.__config.SONGINFO_DURATION,
                              value=f"{duration}",
                              inline=True)
        else:
            embedvc.add_field(name=self.__config.SONGINFO_DURATION,
                              value=self.__config.SONGINFO_UNKNOWN_DURATION,
                              inline=True)

        embedvc.add_field(name=self.__config.SONGINFO_POSITION,
                          value=position,
                          inline=True)

        return embedvc

    async def __timeout_handler(self) -> None:
        if self.__guild.voice_client == None:
            return

        if self.__guild.voice_client.is_playing() or self.__guild.voice_client.is_paused():
            self.__timer = Timer(self.__timeout_handler)

        elif self.__guild.voice_client.is_connected():
            self.__playlist.clear()
            self.__playlist.loop_off()
            await self.__guild.voice_client.disconnect()

    def __ensure_source(self, song: Song) -> str:
        while True:
            if song.source != None:  # If song got downloaded
                return song.source

            if song.problematic:  # If song got any error
                return None
