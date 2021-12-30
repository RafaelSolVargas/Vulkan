import discord
from discord.ext import commands

from config import config
from vulkanbot.music.Downloader import Downloader
from vulkanbot.music.Playlist import Playlist
from vulkanbot.music.Searcher import Searcher
from vulkanbot.music.Types import Provider
from vulkanbot.music.utils import *


class Music(commands.Cog):
    def __init__(self, bot):
        self.__searcher: Searcher = Searcher()
        self.__downloader: Downloader = Downloader()
        self.__playlist: Playlist = Playlist()
        self.__bot: discord.Client = bot

        self.__playing = False
        self.__ffmpeg = 'C:/ffmpeg/bin/ffmpeg.exe'
        self.__vc = ""  # Objeto voice_bot do discord

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'executable': self.__ffmpeg,
                               'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __play_next(self, error, ctx):
        while True:
            if len(self.__playlist) > 0:
                source = self.__playlist.next_song()
                if source == None:  # If there is not a source for the song
                    continue
                    
                coro = self.__play_music(ctx, source)
                self.__bot.loop.create_task(coro)
                break
            else:
                self.__playing = False
                break

    async def __play_music(self, ctx, song):
        self.__playing = True

        player = discord.FFmpegPCMAudio(song.source, **self.FFMPEG_OPTIONS)
        self.__vc.play(player, after=lambda e: self.__play_next(e, ctx))

        await ctx.invoke(self.__bot.get_command('np'))

        songs = self.__playlist.songs_to_preload
        await self.__downloader.preload(songs)

    @commands.command(name="play", help="Toca música - YouTube/Spotify/Título", aliases=['p', 'tocar'])
    async def play(self, ctx, *args):
        user_input = " ".join(args)

        try:
            if len(self.__bot.voice_clients) == 0:
                voice_channel = ctx.author.voice.channel
                self.__vc = await voice_channel.connect()
        except Exception as e:
            print(e)
            await self.__send_embed(ctx, title='Para tocar música, primeiro se conecte a um canal de voz.', colour_name='grey')
            return
        else:
            songs_quant = 0
            musics_identifiers, provider = self.__searcher.search(user_input)
            
            if provider == Provider.Unknown: # If type not identified 
                await self.__send_embed(ctx, description='Entrada inválida, tente algo melhor', colour_name='blue')
                return

            if provider == Provider.YouTube: # If youtube source
                musics_identifiers = self.__downloader.extract_youtube_link(musics_identifiers[0])

            for identifier in musics_identifiers: # Creating songs
                last_song = self.__playlist.add_song(identifier)
                songs_quant += 1

            songs_preload = self.__playlist.songs_to_preload
            await self.__downloader.preload(songs_preload)
            
            if songs_quant == 1: # If only one music downloaded
                song = self.__downloader.download_one(last_song) # Download the new music

                if song == None: # If song not downloaded
                    await self.__send_embed(ctx, description='Houve um problema no download dessa música, tente novamente', colour_name='blue')
                
                elif not self.__playing : # If not playing

                    await self.__send_embed(ctx, description=f'Você adicionou a música **{song.title}** à playlist', colour_name='blue')
                
                else: # If playing
                    await ctx.send(embed=song.embed(title='Song added to Queue'))
            else:
                await self.__send_embed(ctx, description=f"Você adicionou {songs_quant} músicas à fila!", colour_name='blue')

            if not self.__playing:
                first = self.__playlist.songs_to_preload[0]
                self.__downloader.download_one(first)
                first_song = self.__playlist.next_song()

                await self.__play_music(ctx, first_song)

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.", aliases=['q', 'fila'])
    async def queue(self, ctx):
        if self.__playlist.looping_one:  # If Repeating one
            await self.now_playing(ctx)
            return

        songs_preload = self.__playlist.songs_to_preload 
        await self.__downloader.preload(songs_preload)        
        total_time = format_time(sum([int(song.duration if song.duration else 0) for song in songs_preload])) # Sum the duration
        total_songs = len(self.__playlist)
        text = f'Total musics: {total_songs} | Duration: `{total_time}` downloaded  \n\n'

        for pos, song in enumerate(songs_preload, start=1):
            title = song.title if song.title else 'Downloading...'
            text += f"**`{pos}` - ** {title} - `{format_time(song.duration)}`\n"

        if len(songs_preload) > 0:
            if self.__playlist.looping_all:  # If repeating all
                await self.__send_embed(ctx, title='Repeating all', description=text, colour_name='blue')
            else:  # Repeating off
                await self.__send_embed(ctx, title='Songs in Queue', description=text, colour_name='blue')
        else:  # No music
            await self.__send_embed(ctx, description='There is not musics in queue.', colour_name='red')

    @commands.command(name="skip", help="Pula a atual música que está tocando.", aliases=['pular'])
    async def skip(self, ctx):
        if len(self.__bot.voice_clients) > 0:
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

    @commands.command(name='resume', help='Solta a música atual')
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

    @commands.command(name='clear', help='Limpa a fila de músicas a tocar')
    async def clear(self, ctx):
        self.__playlist.clear()

    @commands.command(name='np', help='Mostra a música que está tocando no instante')
    async def now_playing(self, ctx):
        if self.__playlist.looping_one:
            title = 'Song Looping Now'
        else:
            title = 'Song Playing Now'

        current_song = self.__playlist.current
        await ctx.send(embed=current_song.embed(title=title))

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

    @commands.command(name='shuffle', help='Altera aleatoriamente a ordem das músicas')
    async def shuffle(self, ctx):
        self.__playlist.shuffle()
        songs = self.__playlist.songs_to_preload
        
        await self.__downloader.preload(songs)

        await self.__send_embed(ctx, description='Musicas embaralhadas', colour_name='blue')

    @commands.command(name='move', help='Manda uma música de uma posição para outra <from> <to>')
    async def move(self, ctx, pos1, pos2='1'): 
        try:
            pos1 = int(pos1)
            pos2 = int(pos2)

        except Exception as e:
            print(e)
            await ctx.send('This command require a number')
            return

        success, reason = self.__playlist.move_songs(pos1, pos2)

        if not success: 
            songs = self.__playlist.songs_to_preload
            await self.__downloader.preload(songs)
            await ctx.send(reason)
        else:
            await ctx.send(reason)

def setup(bot):
    bot.add_cog(Music(bot))
