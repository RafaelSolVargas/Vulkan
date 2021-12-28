import requests
import json
import discord
from config import config
from discord.ext import commands
from random import random as rand


class Phrases(commands.Cog):
    """Deal with the generation of motivational phrases"""

    def __init__(self, bot):
        self.__bot = bot

    @property
    def bot(self):
        return self.__bot

    @bot.setter
    def bot(self, newBot):
        self.__bot = newBot

    @commands.command(name='frase', help='Envia uma frase pica, talvez a braba')
    async def phrase(self, ctx):
        # There is a chance that the phrase will be send for the dev
        secret = await self.__calculate_rgn()
        if secret != None:
            await ctx.send(secret)
        else:
            phrase = await self.__get_phrase()
            await ctx.send(phrase)

    async def __calculate_rgn(self):
        x = rand()
        if x < 0.15:
            return config.SECRET_MESSAGE
        else:
            return None

    async def __get_phrase(self):
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_PHRASES_TRIES:
                return 'O banco de dados dos cara tá off, bando de vagabundo, tenta depois aí bicho'

            try:
                response = requests.get(config.PHRASES_API)
                data = json.loads(response.content)

                phrase = data['quoteText']
                author = data['quoteAuthor']

                text = f'{phrase} \nBy: {author}'

                return text
            except Exception as e:
                continue


def setup(bot):
    bot.add_cog(Phrases(bot))
