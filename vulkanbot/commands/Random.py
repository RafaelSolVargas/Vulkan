from random import randint, random
import discord
from discord.ext import commands
from config import config

class Random(commands.Cog):
    """Deal with returning random things"""

    def __init__(self, bot):
        self.__bot = bot

    @commands.command(name='random', help=config.HELP_RANDOM)
    async def random(self, ctx, arg: str):
        try:
            arg = int(arg)

        except Exception as e:
            embed = discord.Embed(
                description='Manda um número aí ow animal',
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
            title=f'Número Aleatório entre {a, b}',
            description=x,
            colour=config.COLOURS['green']
        )
        await ctx.send(embed=embed)

    @commands.command(name='cara', help=config.HELP_CARA)
    async def cara(self, ctx):
        x = random()
        if x < 0.5:
            result = 'cara'
        else:
            result = 'coroa'

        embed = discord.Embed(
            title='Cara Cora',
            description=f'Resultado: {result}',
            colour=config.COLOURS['green']
        )
        await ctx.send(embed=embed)

    @commands.command(name='escolha', help=config.HELP_ESCOLHA)
    async def escolher(self, ctx, *args: str):
        try:
            user_input = " ".join(args)
            itens = user_input.split(sep=',')

            index = randint(0, len(itens)-1)

            embed = discord.Embed(
                title='Escolha de algo',
                description=itens[index],
                colour=config.COLOURS['green']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='Escolha de algo',
                description='Erro: Envie várias coisas separadas por vírgula',
                colour=config.COLOURS['green']
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
