import discord
from discord.ext import commands

from config import config
from vulkan.music.Player import Player
from vulkan.music.utils import *


class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.__guilds = {}
        self.__bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.__bot.guilds:
            self.__guilds[guild] = Player(self.__bot, guild)

    @commands.command(name="play", help=config.HELP_PLAY, aliases=['p', 'tocar'])
    async def play(self, ctx, *args) -> None:
        track = " ".join(args)
        requester = ctx.author.name

        player = self.__get_player(ctx)
        if player == None:
            await self.__send_embed(ctx, config.ERROR_TITLE, config.NO_GUILD, 'red')
            return

        if is_connected(ctx) == None:
            success = await player.connect(ctx)
            if success == False:
                await self.__send_embed(ctx, config.ERROR_TITLE, config.NO_CHANNEL, 'red')
                return

        await player.play(ctx, track, requester)

    @commands.command(name="queue", help=config.HELP_QUEUE, aliases=['q', 'fila'])
    async def queue(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return

        embed = await player.queue()
        await ctx.send(embed=embed)

    @commands.command(name="skip", help=config.HELP_SKIP, aliases=['s', 'pular'])
    async def skip(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.skip(ctx)

    @commands.command(name='stop', help=config.HELP_STOP, aliases=['parar'])
    async def stop(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.stop()

    @commands.command(name='pause', help=config.HELP_PAUSE, aliases=['pausar'])
    async def pause(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            success = await player.pause()
            if success:
                await self.__send_embed(ctx, config.SONG_PLAYER, config.SONG_PAUSED, 'blue')

    @commands.command(name='resume', help=config.HELP_RESUME, aliases=['soltar'])
    async def resume(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            success = await player.resume()
            if success:
                await self.__send_embed(ctx, config.SONG_PLAYER, config.SONG_RESUMED, 'blue')

    @commands.command(name='prev', help=config.HELP_PREV, aliases=['anterior'])
    async def prev(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return

        if is_connected(ctx) == None:
            success = await player.connect(ctx)
            if success == False:
                await self.__send_embed(ctx, config.ERROR_TITLE, config.NO_CHANNEL, 'red')
                return

        await player.play_prev(ctx)

    @commands.command(name='history', help=config.HELP_HISTORY, aliases=['historico'])
    async def history(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            embed = player.history()
            await ctx.send(embed=embed)

    @commands.command(name='loop', help=config.HELP_LOOP, aliases=['l', 'repeat'])
    async def loop(self, ctx, args: str) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            description = await player.loop(args)
            await self.__send_embed(ctx, config.SONG_PLAYER, description, 'blue')

    @commands.command(name='clear', help=config.HELP_CLEAR, aliases=['c', 'limpar'])
    async def clear(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.clear()

    @commands.command(name='np', help=config.HELP_NP, aliases=['playing', 'now'])
    async def now_playing(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            embed = await player.now_playing()
            await self.__clean_messages(ctx)
            await ctx.send(embed=embed)

    @commands.command(name='shuffle', help=config.HELP_SHUFFLE, aliases=['aleatorio'])
    async def shuffle(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            description = await player.shuffle()
            await self.__send_embed(ctx, config.SONG_PLAYER, description, 'blue')

    @commands.command(name='move', help=config.HELP_MOVE, aliases=['m', 'mover'])
    async def move(self, ctx, pos1, pos2='1') -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            description = await player.move(pos1, pos2)
            await self.__send_embed(ctx, config.SONG_PLAYER, description, 'blue')

    @commands.command(name='remove', help=config.HELP_REMOVE, aliases=['remover'])
    async def remove(self, ctx, position) -> None:
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            description = await player.remove(position)
            await self.__send_embed(ctx, config.SONG_PLAYER, description, 'blue')

    @commands.command(name='reset', help=config.HELP_RESET, aliases=['resetar'])
    async def reset(self, ctx) -> None:
        player = self.__get_player(ctx)
        if player != None:
            await player.stop()

        self.__guilds[ctx.guild] = Player(self.__bot, ctx.guild)

    async def __send_embed(self, ctx, title='', description='', colour='grey') -> None:
        try:
            colour = config.COLOURS[colour]
        except:
            colour = config.COLOURS['grey']

        embedvc = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )
        await ctx.send(embed=embedvc)

    async def __clean_messages(self, ctx) -> None:
        last_messages = await ctx.channel.history(limit=5).flatten()

        for message in last_messages:
            try:
                if message.author == self.__bot.user:
                    if len(message.embeds) > 0:
                        embed = message.embeds[0]
                        if embed.title in config.SONGS_PLAYING_TITLES:
                            await message.delete()
            except:
                continue

    def __get_player(self, ctx) -> Player:
        try:
            return self.__guilds[ctx.guild]
        except:
            return None


def setup(bot):
    bot.add_cog(Music(bot))
