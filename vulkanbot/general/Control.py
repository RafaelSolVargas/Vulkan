import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from config import config


class Control(commands.Cog):
    """Control the flow of the Bot"""

    def __init__(self, bot):
        self.__bot = bot

    @property
    def bot(self):
        return self.__bot

    @bot.setter
    def bot(self, newBot):
        self.__bot = newBot

    @commands.Cog.listener()
    async def on_ready(self):
        print(config.STARTUP_MESSAGE)
        await self.__bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Vulkan | type {config.BOT_PREFIX}help"))
        print(config.STARTUP_COMPLETE_MESSAGE)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.channel.send(f'Falta argumentos. Digite {config.BOT_PREFIX}help para ver os comandos')
        elif isinstance(error, CommandNotFound):
            await ctx.channel.send(f'O comando não existe')
        else:
            raise error


def setup(bot):
    bot.add_cog(Control(bot))
