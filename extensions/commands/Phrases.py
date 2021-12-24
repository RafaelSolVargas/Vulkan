import requests
import json
import discord
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

    @commands.command(name='frase', help='Envia uma frase legal no seu PV')
    async def send_phrase(self, ctx):
        # There is a chance that the phrase will be send for the dev
        sended = await self.calculate_rgn(ctx)
        if sended:
            return

        while True:
            try:
                response = requests.get(
                    'http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en')
                data = json.loads(response.content)

                phrase = data['quoteText']
                author = data['quoteAuthor']

                text = f'{phrase} \nBy: {author}'
                await ctx.send(text)
                break
            except json.decoder.JSONDecodeError:
                continue
            except discord.errors.Forbidden as e:
                print(e)
                await ctx.channel.send('Não posso te enviar a frase, habilite para receber mensagens de qualquer pessoa no servidor (Opções > Privacidade)')
                break
            except Exception as e:
                print(e)
                await ctx.channel.send('Houve um erro inesperado :/')
                break

    async def calculate_rgn(self, ctx):
        x = rand()
        print(x)
        if x < 0.15:
            await ctx.send('Se leu seu cu é meu\nBy: Minha Pica')
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(Phrases(bot))
