import requests
import json
import discord
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
    async def cetus(self, ctx):
        description = await self.__get_api()
        embed = discord.Embed(
            title='Warframe Cetus Timing',
            description=description,
            colour=config.COLOURS['blue']
        )
        await ctx.send(embed=embed)

    async def __get_api(self):
        """Return the information of the Warframe API"""
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_CETUS_TRIES:
                return 'Os DE baiano não tão com o banco de dados ligado'

            try:
                response = requests.get(config.CETUS_API)
                data = json.loads(response.content)
                short = data['shortString']

                return short

            except Exception as e:
                continue


def setup(bot):
    bot.add_cog(Warframe(bot))
