import discord
import os

from config.Config import Config
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
config = Config()

bot = commands.Bot(command_prefix=config.BOT_PREFIX, pm_help=True,
                   case_insensitive=True, intents=intents)
bot.remove_command('help')

if config.BOT_TOKEN == "":
    exit()

for filename in os.listdir('./vulkan/commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'vulkan.commands.{filename[:-3]}')


bot.run(config.BOT_TOKEN, bot=True, reconnect=True)
