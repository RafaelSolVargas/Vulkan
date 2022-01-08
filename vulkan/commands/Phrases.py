from discord.client import Client
import requests
import json
from config import config
from discord.ext import commands
from random import random as rand


class Phrases(commands.Cog):
    """Deal with the generation of motivational phrases"""

    def __init__(self, bot: Client):
        self.__bot = bot

    @commands.command(name='frase', help=config.HELP_FRASE)
    async def phrase(self, ctx):
        """Send some phrase to the requester"""
        secret = await self.__calculate_rgn()
        if secret != None:
            await ctx.send(secret)
        else:
            phrase = await self.__get_phrase()
            await ctx.send(phrase)

    async def __calculate_rgn(self):
        """Calculate the chance from the phrase function return a secret custom message"""
        x = rand()
        if x < 0.15:
            return config.SECRET_MESSAGE
        else:
            return None

    async def __get_phrase(self):
        """Get the phrase from the server"""
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_PHRASES_TRIES:
                return config.ERROR_WHILE_REQUEST
                return 'O banco de dados dos cara tá off, bando de vagabundo, tenta depois aí bicho'

            try:
                response = requests.get(config.PHRASES_API)
                data = json.loads(response.content)

                phrase = data['quoteText']
                author = data['quoteAuthor']

                if phrase == '' or author == '':
                    continue

                text = f'{phrase} \nBy: {author}'

                return text
            except:
                continue


def setup(bot):
    bot.add_cog(Phrases(bot))
