import discord
from discord import Client
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, CommandInvokeError
from discord.ext import commands
from config import config
from config import help


class Control(commands.Cog):
    """Control the flow of the Bot"""

    def __init__(self, bot: Client):
        self.__bot = bot
        self.__comandos = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop',
                      'skip', 'play', 'queue', 'clear',
                      'np', 'shuffle', 'move', 'remove',
                      'reset', 'prev', 'history'],
            'RANDOM': ['choose', 'cara', 'random']

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
                colour=config.COLOURS['black']
            )
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.COMMAND_NOT_FOUND,
                colour=config.COLOURS['black']
            )
            await ctx.send(embed=embed)
        elif isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                title=config.BAD_COMMAND_TITLE,
                description=config.BAD_COMMAND,
                colour=config.COLOURS['black']
            )
            await ctx.send(embed=embed)

        else:
            print(error)
            embed = discord.Embed(
                title=config.ERROR_TITLE,
                description=config.UNKNOWN_ERROR,
                colour=config.COLOURS['red']
            )
            await ctx.send(embed=embed)

    @commands.command(name="help", help=help.HELP_HELP, description=help.HELP_HELP_LONG, aliases=['h', 'ajuda'])
    async def help_msg(self, ctx, command_help=''):
        if command_help != '':
            for command in self.__bot.commands:
                if command.name == command_help:
                    txt = command.description if command.description else command.help

                    embedhelp = discord.Embed(
                        title=f'**Description of {command_help}** command',
                        description=txt,
                        colour=config.COLOURS['blue']
                    )

                    await ctx.send(embed=embedhelp)
                    return

            embedhelp = discord.Embed(
                title='Command Help',
                description=f'Command {command_help} Not Found',
                colour=config.COLOURS['red']
            )

            await ctx.send(embed=embedhelp)
        else:

            helptxt = ''
            help_music = '🎧 `MUSIC`\n'
            help_random = '🎲 `RANDOM`\n'
            help_help = '👾 `HELP`\n'

            for command in self.__bot.commands:
                if command.name in self.__comandos['MUSIC']:
                    help_music += f'**{command}** - {command.help}\n'

                elif command.name in self.__comandos['RANDOM']:
                    help_random += f'**{command}** - {command.help}\n'

                else:
                    help_help += f'**{command}** - {command.help}\n'

            helptxt = f'\n{help_music}\n{help_help}\n{help_random}'
            helptxt += f'\n\nType {config.BOT_PREFIX}help "command" for more information about the command chosen'
            embedhelp = discord.Embed(
                title=f'**Available Commands of {self.__bot.user.name}**',
                description=helptxt,
                colour=config.COLOURS['blue']
            )

            embedhelp.set_thumbnail(url=self.__bot.user.avatar_url)
            await ctx.send(embed=embedhelp)

    @commands.command(name='invite', help=help.HELP_INVITE, description=help.HELP_INVITE_LONG)
    async def invite_bot(self, ctx):
        invite_url = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot>'.format(
            self.__bot.user.id)
        txt = config.INVITE_MESSAGE.format(invite_url)

        embed = discord.Embed(
            title="Invite Vulkan",
            description=txt,
            colour=config.COLOURS['blue']
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Control(bot))
