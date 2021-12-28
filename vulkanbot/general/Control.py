import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from config import config


class Control(commands.Cog):
    """Control the flow of the Bot"""

    def __init__(self, bot):
        self.__bot = bot
        self.__comandos = {
            'MUSIC': ['this', 'resume', 'pause', 'loop', 'stop', 'skip', 'play', 'queue', 'clear'],
            'RANDOM': ['cetus', ' frase'],
            'HELP': ['help']
        }

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

    @commands.command(name="help", alisases=['ajuda'], help="Comando de ajuda")
    async def help(self, ctx):
        helptxt = ''
        help_music = '-- MUSIC\n'
        help_random = '-- RANDOM\n'
        help_help = '-- HELP\n'

        for command in self.__bot.commands:
            if command.name in self.__comandos['MUSIC']:
                help_music += f'**{command}** - {command.help}\n'
            elif command.name in self.__comandos['HELP']:
                help_help += f'**{command}** - {command.help}\n'
            else:
                help_random += f'**{command}** - {command.help}\n'
        helptxt = f'{help_music}\n{help_random}\n{help_help}'

        embedhelp = discord.Embed(
            colour=config.COLOURS['grey'],
            title=f'Comandos do {self.__bot.user.name}',
            description=helptxt
        )

        embedhelp.set_thumbnail(url=self.__bot.user.avatar_url)
        await ctx.send(embed=embedhelp)

    @commands.Cog.listener()
    async def on_error(self, error):
        print('On Error')


def setup(bot):
    bot.add_cog(Control(bot))
