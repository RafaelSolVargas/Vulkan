import requests
import json
import discord
from discord.ext import commands


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
        while True:
            try:
                response = requests.get(
                    'http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en')
                data = json.loads(response.content)

                phrase = data['quoteText']
                author = data['quoteAuthor']

                text = f'{phrase} \nBy: {author}'
                await ctx.author.send(text)
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


def setup(bot):
    bot.add_cog(Phrases(bot))
