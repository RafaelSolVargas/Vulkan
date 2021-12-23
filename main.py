import os
import discord
from dotenv import dotenv_values
from discord.ext import commands

TOKEN_BOT = dotenv_values('.env')['TOKEN_BOT']

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!",
                      case_insensitive=True, intents=intents)
client.remove_command('help')


def load_cogs(bot):
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


load_cogs(client)
client.run(TOKEN_BOT)
