import discord
from discord.ext import commands
from config import config
import datetime

from vulkan.music.Downloader import Downloader
from vulkan.music.Playlist import Playlist
from vulkan.music.Searcher import Searcher
from vulkan.music.Types import Provider
from vulkan.music.utils import *


class Player(commands.Cog):
    def __init__(self, bot, guild):
        self.__searcher: Searcher = Searcher()
        self.__down: Downloader = Downloader()
        self.__playlist: Playlist = Playlist()
        self.__bot: discord.Client = bot
        self.__guild: discord.Guild = guild

        self.__timer = Timer(self.__timeout_handler)
        self.__playing = False

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    async def connect(self, ctx):
        if not ctx.author.voice:
            return {'success': False, 'reason': config.NO_CHANNEL}

        if self.__guild.voice_client == None:
            await ctx.author.voice.channel.connect(reconnect=True, timeout=None)
            return {'success': True, 'reason': ''}

    def __play_next(self, error, ctx):
        song = self.__playlist.next_song()
        if song != None:  # If there is not a song for the song
            coro = self.__play_music(ctx, song)
            self.__bot.loop.create_task(coro)
        else:
            self.__playing = False

    async def __play_music(self, ctx, song):
        self.__playing = True

        player = discord.FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
        self.__guild.voice_client.play(
            player, after=lambda e: self.__play_next(e, ctx))

        self.__timer.cancel()
        self.__timer = Timer(self.__timeout_handler)

        await ctx.invoke(self.__bot.get_command('np'))

        songs = self.__playlist.songs_to_preload
        await self.__down.preload(songs)

    async def play(self, ctx, track, requester) -> str:
        try:
            songs_names, provider = self.__searcher.search(track)
            if provider == Provider.Unknown:
                embed = discord.Embed(
                    title=config.ERROR_TITLE,
                    description=config.INVALID_INPUT,
                    colours=config.COLOURS['blue'])
                await ctx.send(embed=embed)
                return

            elif provider == Provider.YouTube:
                songs_names = self.__down.extract_youtube_link(songs_names[0])

            songs_quant = 0
            for name in songs_names:
                song = self.__playlist.add_song(name, requester)
                songs_quant += 1

            songs_preload = self.__playlist.songs_to_preload
            await self.__down.preload(songs_preload)

        except:
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.DOWNLOADING_ERROR,
                colours=config.COLOURS['blue'])
            await ctx.send(embed=embed)
            return

        if songs_quant == 1:
            song = self.__down.download_one(song)

            if song == None:
                embed = discord.Embed(
                    title=config.ERROR_TITLE,
                    description=config.DOWNLOADING_ERROR,
                    colours=config.COLOURS['blue'])
                await ctx.send(embed=embed)
                return
            elif not self.__playing:
                embed = discord.Embed(
                    title=config.SONG_QUEUE_TITLE,
                    description=config.SONG_ADDED.format(song.title),
                    colour=config.COLOURS['blue'])
                await ctx.send(embed=embed)
            else:
                embed = self.__format_embed(song.info, config.SONG_ADDED)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=config.SONG_QUEUE_TITLE,
                description=config.SONGS_ADDED.format(songs_quant),
                colour=config.COLOURS['blue'])
            await ctx.send(embed=embed)

        if not self.__playing:
            try_another = True

            while try_another:  # This will ensure the first song source to be ready
                first_song = self.__playlist.next_song()
                if first_song == None:
                    embed = discord.Embed(
                        title=config.ERROR_TITLE,
                        description=config.DOWNLOADING_ERROR,
                        colour=config.COLOURS['blue'])
                    await ctx.send(embed=embed)
                    break

                while True:
                    if first_song.source != None:  # If song got downloaded
                        try_another = False
                        break

                    if first_song.problematic:  # If song got any error, try another one
                        break

            if first_song != None:
                await self.__play_music(ctx, first_song)

    async def queue(self) -> discord.Embed:
        if self.__playlist.looping_one:
            info = self.__playlist.current.info
            title = 'Song Looping Now'
            return self.__format_embed(info, title)

        songs_preload = self.__playlist.songs_to_preload
        await self.__down.preload(songs_preload)
        total_time = format_time(sum([int(song.duration if song.duration else 0)
                                 for song in songs_preload]))  # Sum the duration
        total_songs = len(self.__playlist)
        text = f'Total musics: {total_songs} | Duration: `{total_time}` downloaded  \n\n'

        for pos, song in enumerate(songs_preload, start=1):
            title = song.title if song.title else 'Downloading...'
            text += f"**`{pos}` - ** {title} - `{format_time(song.duration)}`\n"

        title = 'Songs in Queue'
        if len(songs_preload) > 0:
            if self.__playlist.looping_all:
                title = 'Repeating All'
        else:
            text = 'There is no musics in queue'

        embed = discord.Embed(
            title=title,
            description=text,
            colour=config.COLOURS['blue']
        )

        return embed

    async def skip(self) -> bool:
        if self.__guild.voice_client != None:
            self.__guild.voice_client.stop()
            return True
        else:
            return False

    async def stop(self) -> bool:
        if self.__guild.voice_client == None:
            return False

        if self.__guild.voice_client.is_connected():
            self.__playlist.clear()
            self.__playlist.loop_off()
            self.__guild.voice_client.stop()
            await self.__guild.voice_client.disconnect()
            return True

    async def pause(self) -> bool:
        if self.__guild.voice_client == None:
            return False

        if self.__guild.voice_client.is_playing():
            self.__guild.voice_client.pause()
            return True

    async def resume(self) -> bool:
        if self.__guild.voice_client == None:
            return False

        if self.__guild.voice_client.is_paused():
            self.__guild.voice_client.resume()
            return True

    async def loop(self, args: str):
        args = args.lower()
        if args == 'one':
            description = self.__playlist.loop_one()
        elif args == 'all':
            description = self.__playlist.loop_all()
        elif args == 'off':
            description = self.__playlist.loop_off()
        else:
            description = 'Comando Loop\nOne - Repete a música atual\nAll - Repete as músicas atuais\nOff - Desativa o loop'

        return description

    async def clear(self) -> None:
        self.__playlist.clear()

    async def now_playing(self) -> discord.Embed:
        if self.__playlist.looping_one:
            title = 'Song Looping Now'
        else:
            title = 'Song Playing Now'

        current_song = self.__playlist.current
        embed = self.__format_embed(current_song.info, title)

        return embed

    async def shuffle(self) -> str:
        try:
            self.__playlist.shuffle()
            songs = self.__playlist.songs_to_preload

            await self.__down.preload(songs)
            return 'Musics shuffled successfully'
        except:
            return 'An error ocurred :/'

    async def move(self, pos1, pos2='1') -> str:
        try:
            pos1 = int(pos1)
            pos2 = int(pos2)

        except:
            return 'This command require a number'

        result = self.__playlist.move_songs(pos1, pos2)

        songs = self.__playlist.songs_to_preload
        await self.__down.preload(songs)
        return result

    async def remove(self, position) -> str:
        """Remove a song from the queue in the position"""
        try:
            position = int(position)

        except:
            return 'This command require a number'

        result = self.__playlist.remove_song(position)
        return result

    def __format_embed(self, info, title='') -> discord.Embed:
        """Configure the embed to show the song information"""
        embedvc = discord.Embed(
            title=title,
            description=f"[{info['title']}]({info['original_url']})",
            color=config.COLOURS['blue']
        )

        embedvc.add_field(name=config.SONGINFO_UPLOADER,
                          value=info['uploader'],
                          inline=True)

        embedvc.add_field(name=config.SONGINFO_REQUESTER,
                          value=info['requester'],
                          inline=True)

        if 'thumbnail' in info.keys():
            embedvc.set_thumbnail(url=info['thumbnail'])

        if 'duration' in info.keys():
            duration = str(datetime.timedelta(seconds=info['duration']))
            embedvc.add_field(name=config.SONGINFO_DURATION,
                              value=f"{duration}",
                              inline=True)
        else:
            embedvc.add_field(name=config.SONGINFO_DURATION,
                              value=config.SONGINFO_UNKNOWN_DURATION,
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
