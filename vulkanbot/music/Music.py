import discord
from discord.ext import commands
import datetime
import asyncio

from config import config
from vulkanbot.music.Downloader import Downloader
from vulkanbot.music.Playlist import Playlist
from vulkanbot.music.Searcher import Searcher


class Music(commands.Cog):
    def __init__(self, bot):
        self.__searcher = Searcher()
        self.__downloader = Downloader()
        self.__playlist = Playlist()

        self.__playing = False
        self.__bot = bot
        self.__ffmpeg = 'C:/ffmpeg/bin/ffmpeg.exe'
        self.__vc = ""  # Objeto voice_bot do discord

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'executable': self.__ffmpeg,
                               'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __play_next(self):
        while True:
            if len(self.__playlist) > 0:
                source = self.__playlist.next_song()
                if source == None:  # If there is not a source
                    continue

                player = discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS)
                self.__vc.play(player, after=lambda e: self.__play_next())
                break
            else:
                self.__playing = False
                break

    # infinite loop checking
    async def __play_music(self):
        while True:
            if len(self.__playlist) > 0:
                source = self.__playlist.next_song()
                if source == None:
                    continue

                self.__playing = True
                player = discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS)
                self.__vc.play(player, after=lambda e: self.__play_next())
                break
            else:
                self.__playing = False
                await self.__vc.disconnect()
                break

    @commands.command(name="play", help="Toca música - YouTube/Spotify/Título", aliases=['p', 'tocar'])
    async def play(self, ctx, *args):
        user_input = " ".join(args)

        try:
            if self.__vc == "" or not self.__vc.is_connected() or self.__vc == None:
                voice_channel = ctx.author.voice.channel
                self.__vc = await voice_channel.connect()
        except Exception as e:
            # If voice_channel is None:
            print(e)
            await self.__send_embed(ctx, title='Para tocar música, primeiro se conecte a um canal de voz.', colour_name='grey')
            return
        else:
            songs_quant = 0
            musics_names, provider = self.__searcher.search(user_input)
            for music in musics_names:
                music_info = self.__downloader.download_urls(music, provider)

                for music in music_info:
                    self.__playlist.add_song(music)
                    songs_quant += 1

            if songs_quant == 1:
                await self.__send_embed(ctx, description=f"Você adicionou a música **{music_info[0]['title']}** à fila!", colour_name='green')
            else:
                await self.__send_embed(ctx, description=f"Você adicionou {songs_quant} músicas à fila!", colour_name='green')

            if not self.__playing:
                await self.__play_music()

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.", aliases=['q', 'fila'])
    async def queue(self, ctx):
        if self.__playlist.looping_one:  # If Repeting one
            # Send the current song with this title
            await self.this(ctx)
            return

        fila = self.__playlist.queue()
        total = len(fila)
        text = f'Total musics: {total}\n\n'

        # Create the string to description
        for pos, song in enumerate(fila):
            if pos >= config.MAX_QUEUE_LENGTH:  # Max songs to apper in queue list
                break

            text += f"**{pos+1} - ** {song}\n"

        if text != "":
            if self.__playlist.looping_all:  # If repeting all
                await self.__send_embed(ctx, title='Repeating all', description=text, colour_name='green')
            else:  # Repeting off
                await self.__send_embed(ctx, title='Queue', description=text, colour_name='green')
        else:  # No music
            await self.__send_embed(ctx, description='There is not musics in queue.', colour_name='red')

    @commands.command(name="skip", help="Pula a atual música que está tocando.", aliases=['pular'])
    async def skip(self, ctx):
        if self.__vc != '' and self.__vc:
            print('Skip')
            self.__vc.stop()

    @commands.command(name='stop', help='Para de tocar músicas')
    async def stop(self, ctx):
        if self.__vc == '':
            return
        if self.__vc.is_connected():
            self.__playlist.clear()
            self.__vc.stop()
            await self.__vc.disconnect()

    @commands.command(name='pause', help='Pausa a música')
    async def pause(self, ctx):
        if self.__vc == '':
            return
        if self.__vc.is_playing():
            self.__vc.pause()
            await self.__send_embed(ctx, description='Música pausada', colour_name='green')

    @commands.command(name='resume', help='Despausa a música atual')
    async def resume(self, ctx):
        if self.__vc == '':
            return
        if self.__vc.is_paused():
            self.__vc.resume()
            await self.__send_embed(ctx, description='Música tocando', colour_name='green')

    @commands.command(name='loop', help='Controla a repetição de músicas')
    async def loop(self, ctx, args: str):
        args = args.lower()
        if args == 'one':
            description = self.__playlist.loop_one()
        elif args == 'all':
            description = self.__playlist.loop_all()
        elif args == 'off':
            description = self.__playlist.loop_off()
        else:
            description = 'Comando Loop\nOne - Repete a música atual\nAll - Repete as músicas atuais\nOff - Desativa o loop'

        await self.__send_embed(ctx, description=description, colour_name='grey')


    async def __send_embed(self, ctx, title='', description='', colour_name='grey'):
        try:
            colour = config.COLOURS[colour_name]
        except Exception as e:
            colour = config.COLOURS['grey']

        embedvc = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )
        await ctx.send(embed=embedvc)

    @commands.command(name='clear', help='Limpa a fila de músicas a tocar')
    async def clear(self, ctx):
        self.__playlist.clear()

    @commands.command(name='this', help='Mostra a música que está tocando no instante')
    async def this(self, ctx):
        if self.__playlist.looping_one:
            title = 'Music Looping Now'
        else:
            title = 'Music Playing Now'

        info = self.__playlist.get_current()
        embedvc = discord.Embed(
            title=title,
            description=f"[{info['title']}]({info['url']})",
            color=config.COLOURS['grey']
        )

        embedvc.add_field(name=config.SONGINFO_UPLOADER,
                          value=info['uploader'],
                          inline=False)

        if 'thumbnail' in info.keys():
            embedvc.set_thumbnail(url=info['thumbnail'])

        if 'duration' in info.keys():
            duration = str(datetime.timedelta(seconds=info['duration']))
            embedvc.add_field(name=config.SONGINFO_DURATION,
                              value=f"{duration}",
                              inline=False)
        else:
            embedvc.add_field(name=config.SONGINFO_DURATION,
                              value=config.SONGINFO_UNKNOWN_DURATION,
                              inline=False)

        await ctx.send(embed=embedvc)


def setup(bot):
    bot.add_cog(Music(bot))
