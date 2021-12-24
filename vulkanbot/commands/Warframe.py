import requests
import json
import discord
from dotenv import dotenv_values
from discord.ext import commands
from config import config


class Warframe(commands.Cog):
    """Deal with the generation of warframe data"""

    def __init__(self, bot):
        self.__bot = bot

    @property
    def bot(self):
        return self.__bot

    @bot.setter
    def bot(self, newBot):
        self.__bot = newBot

    @commands.command(name='cetus', help='Informa o tempo atual de Cetus - Warframe')
    async def get_cetus(self, ctx):
        try:
            response = requests.get(config.CETUS_API)
            data = json.loads(response.content)
            short = data['shortString']

            responseText = f'{short}'

            embed = discord.Embed(
                title='Warframe Cetus Timing',
                description=responseText,
                colour=0xFF0000
            )
            await ctx.send(embed=embed)

        except Exception as e:
            print(e)
            responseText = f'Houve um erro inesperado :/'
            embed = discord.Embed(
                title='Warframe Cetus Timing',
                description=responseText,
                colour=0xFF0000
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Warframe(bot))
