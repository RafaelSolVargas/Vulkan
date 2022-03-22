import discord
import os

from Config.Config import Configs
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
config = Configs()

bot = commands.Bot(command_prefix=config.BOT_PREFIX, pm_help=True,
                   case_insensitive=True, intents=intents)
bot.remove_command('help')

if config.BOT_TOKEN == "":
    exit()

for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.{filename[:-3]}')


bot.run(config.BOT_TOKEN, bot=True, reconnect=True)
