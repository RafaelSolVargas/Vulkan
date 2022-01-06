import os
import discord

from config import config
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, pm_help=True,
                   case_insensitive=True, intents=intents)
bot.remove_command('help')


if __name__ == '__main__':
    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit()

    for extension in config.INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

    bot.run(config.BOT_TOKEN, bot=True, reconnect=True)
