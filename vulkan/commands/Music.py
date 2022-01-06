import discord
from discord.ext import commands

from config import config
from vulkan.music.Player import Player
from vulkan.music.utils import *


class Music(commands.Cog):
    def __init__(self, bot):
        self.__guilds = {}
        self.__bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.__bot.guilds:
            self.__guilds[guild] = Player(self.__bot, guild)

    @commands.command(name="play", help=config.HELP_PLAY, aliases=['p', 'tocar'])
    async def play(self, ctx, *args):
        user_input = " ".join(args)

        player = self.__get_player(ctx)
        if player == None:
            await self.__send_embed(ctx, description=config.NO_GUILD, colour_name='red')
            return

        if is_connected(ctx) == None:
            result = await player.connect(ctx)
            if result['success'] == False:
                await self.__send_embed(ctx, description=result['reason'], colour_name='red')
                return

        await player.play(ctx, user_input)

    @commands.command(name="queue", help=config.HELP_QUEUE, aliases=['q', 'fila'])
    async def queue(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return

        embed = await player.queue()
        await ctx.send(embed=embed)

    @commands.command(name="skip", help=config.HELP_SKIP, aliases=['pular'])
    async def skip(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.skip()

    @commands.command(name='stop', help=config.HELP_STOP, aliases=['parar'])
    async def stop(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.stop()

    @commands.command(name='pause', help=config.HELP_PAUSE, aliases=['pausar'])
    async def pause(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            print('No player')
            return
        else:
            success = await player.pause()
            if success:
                await self.__send_embed(ctx, description='Song paused', colour_name='blue')

    @commands.command(name='resume', help=config.HELP_RESUME, aliases=['soltar'])
    async def resume(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            success = await player.resume()
            if success:
                await self.__send_embed(ctx, description='Song Playing', colour_name='blue')

    @commands.command(name='loop', help=config.HELP_LOOP, aliases=['repeat'])
    async def loop(self, ctx, args: str):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            result = await player.loop(args)
            await self.__send_embed(ctx, description=result, colour_name='blue')

    @commands.command(name='clear', help=config.HELP_CLEAR, aliases=['limpar'])
    async def clear(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            await player.clear()

    @commands.command(name='np', help=config.HELP_NP, aliases=['playing', 'now'])
    async def now_playing(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            embed = await player.now_playing()
            await self.__clean_messages(ctx)
            await ctx.send(embed=embed)

    @commands.command(name='shuffle', help=config.HELP_SHUFFLE, aliases=['aleatorio'])
    async def shuffle(self, ctx):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            result = await player.shuffle()
            await self.__send_embed(ctx, description=result, colour_name='blue')

    @commands.command(name='move', help=config.HELP_MOVE, aliases=['mover'])
    async def move(self, ctx, pos1, pos2='1'):
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            result = await player.move(pos1, pos2)
            await self.__send_embed(ctx, description=result, colour_name='blue')

    @commands.command(name='remove', help=config.HELP_REMOVE, aliases=['remover'])
    async def remove(self, ctx, position):
        """Remove a song from the queue in the position"""
        player = self.__get_player(ctx)
        if player == None:
            return
        else:
            result = await player.remove(position)
            await self.__send_embed(ctx, description=result, colour_name='blue')

    @commands.command(name='reset', help=config.HELP_RESET, aliases=['resetar'])
    async def reset(self, ctx):
        player = self.__get_player(ctx)
        if player != None:
            await player.stop()

        self.__guilds[ctx.guild] = Player(self.__bot, ctx.guild)

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

    async def __clean_messages(self, ctx):
        """Clear Bot messages if send recently"""
        last_messages = await ctx.channel.history(limit=5).flatten()

        for message in last_messages:
            try:
                if message.author == self.__bot.user:
                    if len(message.embeds) > 0:
                        embed = message.embeds[0]
                        if embed.title == 'Song Playing Now' or embed.title == 'Song Looping Now':
                            await message.delete()
            except:
                continue

    def __get_player(self, ctx):
        try:
            return self.__guilds[ctx.guild]
        except:
            return None


def setup(bot):
    bot.add_cog(Music(bot))
