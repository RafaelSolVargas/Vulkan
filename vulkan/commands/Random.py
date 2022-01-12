from random import randint, random
import discord
from discord.ext import commands
from config import config
from config import help


class Random(commands.Cog):
    """Deal with returning random things"""

    def __init__(self, bot):
        self.__bot = bot

    @commands.command(name='random', help=help.HELP_RANDOM, description=help.HELP_RANDOM_LONG)
    async def random(self, ctx, arg: str) -> None:
        try:
            arg = int(arg)

        except:
            embed = discord.Embed(
                description=config.ERROR_NUMBER,
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)
            return

        if arg < 1:
            a = arg
            b = 1
        else:
            a = 1
            b = arg

        x = randint(a, b)
        embed = discord.Embed(
            title=f'Random number between [{a, b}]',
            description=x,
            colour=config.COLOURS['green']
        )
        await ctx.send(embed=embed)

    @commands.command(name='cara', help=help.HELP_CARA, description=help.HELP_CARA_LONG)
    async def cara(self, ctx) -> None:
        x = random()
        if x < 0.5:
            result = 'cara'
        else:
            result = 'coroa'

        embed = discord.Embed(
            title='Cara Cora',
            description=f'Result: {result}',
            colour=config.COLOURS['green']
        )
        await ctx.send(embed=embed)

    @commands.command(name='choose', help=help.HELP_CHOOSE, description=help.HELP_CHOOSE_LONG)
    async def choose(self, ctx, *args: str) -> None:
        try:
            user_input = " ".join(args)
            itens = user_input.split(sep=',')

            index = randint(0, len(itens)-1)

            embed = discord.Embed(
                title='Choose something',
                description=itens[index],
                colour=config.COLOURS['green']
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title='Choose something.',
                description=f'Error: Use {config.BOT_PREFIX}help choose to understand this command.',
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
