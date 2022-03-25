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

    async def connect(self, ctx: Context) -> bool:
        if not ctx.author.voice:
            return False

        if self.__guild.voice_client == None:
            await ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            return True

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

    async def play(self, ctx: Context, track: str, requester: str) -> str:
        try:
            links, provider = self.__searcher.search(track)
            if provider == Provider.Unknown or links == None:
                embed = Embed(
                    title=self.__config.ERROR_TITLE,
                    description=self.__config.INVALID_INPUT,
                    colours=self.__config.COLOURS['blue'])
                await ctx.send(embed=embed)
                return None

            if provider == Provider.YouTube:
                links = await self.__down.extract_info(links[0])

            if len(links) == 0:
                embed = Embed(
                    title=self.__config.ERROR_TITLE,
                    description="This video is unavailable",
                    colours=self.__config.COLOURS['blue'])
                await ctx.send(embed=embed)
                return None

            songs_quant = 0
            for info in links:
                song = self.__playlist.add_song(info, requester)
                songs_quant += 1

            songs_preload = self.__playlist.songs_to_preload
            await self.__down.preload(songs_preload)
        except Exception as e:
            print(f'DEVELOPER NOTE -> Error while Downloading in Player: {e}')
            embed = Embed(
                title=self.__config.ERROR_TITLE,
                description=self.__config.DOWNLOADING_ERROR,
                colours=self.__config.COLOURS['blue'])
            await ctx.send(embed=embed)
            return

        if songs_quant == 1:
            song = self.__down.finish_one_song(song)
            pos = len(self.__playlist)

            if song.problematic:
                embed = Embed(
                    title=self.__config.ERROR_TITLE,
                    description=self.__config.DOWNLOADING_ERROR,
                    colours=self.__config.COLOURS['blue'])
                await ctx.send(embed=embed)
                return None
            elif not self.__playing:
                embed = Embed(
                    title=self.__config.SONG_PLAYER,
                    description=self.__config.SONG_ADDED.format(song.title),
                    colour=self.__config.COLOURS['blue'])
                await ctx.send(embed=embed)
            else:
                embed = self.__format_embed(song.info, self.__config.SONG_ADDED_TWO, pos)
                await ctx.send(embed=embed)
        else:
            embed = Embed(
                title=self.__config.SONG_PLAYER,
                description=self.__config.SONGS_ADDED.format(songs_quant),
                colour=self.__config.COLOURS['blue'])
            await ctx.send(embed=embed)

        if not self.__playing:
            first_song = self.__playlist.next_song()
            await self.__play_music(ctx, first_song)

    async def play_prev(self, ctx: Context) -> None:
        """Stop the currently playing cycle, load the previous song and play"""
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

    async def stop(self) -> bool:
        if self.__guild.voice_client is None:
            return False

        if self.__guild.voice_client.is_connected():
            self.__playlist.clear()
            self.__playlist.loop_off()
            self.__guild.voice_client.stop()
            await self.__guild.voice_client.disconnect()
            return True

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

    def __format_embed(self, info: dict, title='', position='Playing Now') -> Embed:
        """Configure the embed to show the song information"""
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
