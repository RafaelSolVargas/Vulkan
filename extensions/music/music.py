import discord
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import command
from youtube_dl import YoutubeDL

colours = {
    'red': 0xDC143C,
    'green': 0x00FF7F,
    'grey': 0x708090,
    'blue': 0x0000CD
}


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_playing = False
        self.repetingOne = False
        self.repetingAll = False
        self.current = ()
        # 2d array containing [song, channel]
        # self.music_queue vai conter as buscas recebidas feitas no youtube em ordem
        # Caminho do executável para rodar na minha máquina
        self.ffmpeg = 'C:/ffmpeg/bin/ffmpeg.exe'
        # Segue o padrão de [[{'source', 'title'}, canal], [musica, canal]]
        self.music_queue = []
        self.vc = ""  # Objeto voice_client do discord
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'executable': self.ffmpeg,
                               'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:  # Busca um video no youtube e traz o titulo e a fonte dele em formato de dict
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]

            except Exception:
                return False
        # Retorna a fonte e o titulo buscado
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            if self.repetingOne:
                # Coloca a musica atual no topo da fila
                self.music_queue.insert(0, self.current)
            elif self.repetingAll:
                # Joga a musica atual para o final da fila
                self.music_queue.append(self.current)

            self.is_playing = True
            source = self.music_queue[0][0]['source']
            self.current = self.music_queue[0]  # Update current music
            self.music_queue.pop(0)  # Remove from the queue
            player = discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS)
            self.vc.play(player, after=lambda e: self.play_next())  # Play
        else:
            self.is_playing = False
            self.repetingAll = False
            self.repetingOne = False

    # infinite loop checking
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            source = self.music_queue[0][0]['source']

            # Try to connect to voice channel if you are not already connected
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                # Conecta o voice_client no channel da primeira música da lista
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.current = self.music_queue[0]  # Update current music
            self.music_queue.pop(0)  # Remove from the queue
            player = discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTIONS)
            # Start the player
            self.vc.play(player, after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await self.vc.disconnect()

    @commands.command(name="help", alisases=['ajuda'], help="Comando de ajuda")
    async def ajuda(self, ctx):
        helptxt = ''
        for command in self.client.commands:
            helptxt += f'**{command}** - {command.help}\n'
        embedhelp = discord.Embed(
            colour=1646116,  # grey
            title=f'Comandos do {self.client.user.name}',
            description=helptxt
        )
        embedhelp.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embedhelp)

    @commands.command(name="play", help="Toca uma música do YouTube", aliases=['p', 'tocar'])
    async def p(self, ctx, *args):
        query = " ".join(args)

        try:
            # Nome do canal de voz que vai entrar
            voice_channel = ctx.author.voice.channel
        except:
            # If voice_channel is None:
            await self.send_embed(ctx, title='Para tocar música, primeiro se conecte a um canal de voz.', colour_name='grey')
            return
        else:
            song = self.search_yt(query)
            if type(song) == type(True):  # Caso seja retornado um booleano da busca
                await self.send_embed(ctx, description='Algo deu errado! Tente escrever o nome da música novamente!', colour_name='red')
                return
            else:
                await self.send_embed(ctx, description=f"Você adicionou a música **{song['title']}** à fila!", colour_name='green')
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.", aliases=['q', 'fila'])
    async def q(self, ctx):
        fila = ""
        for x in range(len(self.music_queue)):
            fila += f"**{x+1} - ** {self.music_queue[x][0]['title']}\n"

        if self.repetingOne:  # If Repeting one
            await self.send_embed(ctx, title='Repeting One Music',
                                  description=f'Música: **{self.current[0]["title"]}**', colour_name='green')
        elif fila != "":
            if self.repetingAll:  # If repeting all
                await self.send_embed(ctx, title='Repetindo todas', description=fila, colour_name='green')
            else:  # Repeting off
                await self.send_embed(ctx, description=fila, colour_name='green')
        else:  # No music
            await self.send_embed(ctx, description='Não existem músicas na fila.', colour_name='red')

    @commands.command(name="skip", help="Pula a atual música que está tocando.", aliases=['pular'])
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.send_embed(ctx, description=f'Você pulou a música\nRepetindo Uma: {self.repetingOne} \
                                \nRepetindo Todas: {self.repetingAll}', colour_name='green')

    @commands.command(name='stop', help='Para de tocar músicas')
    async def stop(self, ctx):
        if self.vc == '':
            return
        if self.vc.is_connected():
            # Remove todas as músicas da lista
            self.music_queue = []
            self.current = ()
            self.repetingOne = False
            self.repetingAll = False
            self.is_playing = False
            self.vc.stop()
            await self.vc.disconnect()

    @commands.command(name='pause', help='Pausa a música')
    async def pause(self, ctx):
        if self.vc == '':
            return
        if self.vc.is_playing():
            self.vc.pause()
            await self.send_embed(ctx, description='Música pausada', colour_name='green')

    @commands.command(name='resume', help='Despausa a música atual')
    async def resume(self, ctx):
        if self.vc == '':
            return
        if self.vc.is_paused():
            self.vc.resume()
            await self.send_embed(ctx, description='Música tocando', colour_name='green')

    @commands.command(name='repeat_one', help='Repete a música atual')
    async def repeat_one(self, ctx):
        if not self.is_playing:  # Garante que o Bot está tocando
            await self.send_embed(ctx, title='Vulkan não está tocando agora', colour_name='red')
            return

        if self.repetingAll:  # Verifica se o repeting all não está ligado
            await self.send_embed(ctx, title='Já está repetindo todas', colour_name='red')
            return
        else:  # Liga o repeting one
            self.repetingOne = True
            await self.send_embed(ctx, description='Repetir uma música ligado', colour_name='green')

    @commands.command(name='repeat_all', help='Repete toda a fila')
    async def repeat_all(self, ctx):
        if not self.is_playing:  # Garante que o Bot está tocando
            await self.send_embed(ctx, title='Vulkan não está tocando agora', colour_name='red')
            return

        if self.repetingOne:  # Verifica se o repeting all não está ligado
            await self.send_embed(ctx, title='Já está repetindo uma música', colour_name='red')
            return
        else:  # Liga o repeting one
            self.repetingAll = True
            await self.send_embed(ctx, description='Repetir todas as músicas ligado', colour_name='green')

    @commands.command(name='repeat_off', help='Desativa o repetir músicas')
    async def repeat_off(self, ctx):
        if not self.is_playing:  # Garante que o Bot está tocando
            await self.send_embed(ctx, title='Vulkan não está tocando agora', colour_name='red')
            return
        else:
            self.repetingOne = False
            self.repetingAll = False
            await self.send_embed(ctx, description='Repetir músicas desligado', colour_name='green')

    @skip.error  # Erros para kick
    async def skip_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embedvc = discord.Embed(
                colour=12255232,
                description=f"Você precisa da permissão **Gerenciar canais** para pular músicas."
            )
            await ctx.send(embed=embedvc)
        else:
            raise error

    async def send_embed(self, ctx, title='', description='', colour_name='red'):
        try:
            colour = colours[colour_name]
        except Exception as e:
            colour = colours['red']

        embedvc = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )
        await ctx.send(embed=embedvc)


def setup(client):
    client.add_cog(Music(client))
