import discord
from discord import Client
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from config import config


class Control(commands.Cog):
    """Control the flow of the Bot"""

    def __init__(self, bot: Client):
        self.__bot = bot
        self.__comandos = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop', 'skip', 'play', 'queue', 'clear', 'np', 'shuffle', 'move', 'remove', 'reset'],
            'WARFRAME': ['warframe'],
            'RANDOM': ['escolha', 'cara', 'random'],
            'HELP': ['help'],
            'OTHERS': ['frase']
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(config.STARTUP_MESSAGE)
        await self.__bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Vulkan | {config.BOT_PREFIX}help"))
        print(config.STARTUP_COMPLETE_MESSAGE)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.ERROR_MISSING_ARGUMENTS,
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.COMMAND_NOT_FOUND,
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.UNKNOWN_ERROR,
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)

    @commands.command(name="help", help=config.HELP_HELP, aliases=['h', 'ajuda'])
    async def help_msg(self, ctx):
        helptxt = ''
        help_music = '🎧 `MUSIC`\n'
        help_random = '🎲 `RANDOM`\n'
        help_warframe = '🎮 `WARFRAME`\n'
        help_help = '👾 `HELP`\n'
        help_others = '🕹️ `OTHERS`\n'

        for command in self.__bot.commands:
            if command.name in self.__comandos['MUSIC']:
                help_music += f'**{command}** - {command.help}\n'
            elif command.name in self.__comandos['HELP']:
                help_help += f'**{command}** - {command.help}\n'
            elif command.name in self.__comandos['OTHERS']:
                help_others += f'**{command}** - {command.help}\n'
            elif command.name in self.__comandos['WARFRAME']:
                help_warframe += f'**{command}** - {command.help}\n'
            else:
                help_random += f'**{command}** - {command.help}\n'

        helptxt = f'{help_music}\n{help_warframe}\n{help_random}\n{help_others}\n{help_help}'

        embedhelp = discord.Embed(
            title=f'**Available Commands of {self.__bot.user.name}**',
            description=helptxt,
            colour=config.COLOURS['blue']
        )

        embedhelp.set_thumbnail(url=self.__bot.user.avatar_url)
        await ctx.send(embed=embedhelp)


def setup(bot):
    bot.add_cog(Control(bot))
