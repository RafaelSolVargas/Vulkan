import discord
from discord import Client
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, UserInputError
from discord.ext import commands
from Config.Config import Configs
from Config.Helper import Helper

helper = Helper()


class Control(commands.Cog):
    """Control the flow of the Bot"""

    def __init__(self, bot: Client):
        self.__bot = bot
        self.__config = Configs()
        self.__comandos = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop',
                      'skip', 'play', 'queue', 'clear',
                      'np', 'shuffle', 'move', 'remove',
                      'reset', 'prev', 'history'],
            'RANDOM': ['choose', 'cara', 'random']

        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__config.STARTUP_MESSAGE)
        await self.__bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Vulkan | {self.__config.BOT_PREFIX}help"))
        print(self.__config.STARTUP_COMPLETE_MESSAGE)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title=self.__config.ERROR_TITLE,
                description=self.__config.ERROR_MISSING_ARGUMENTS,
                colour=self.__config.COLOURS['black']
            )
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = discord.Embed(
                title=self.__config.ERROR_TITLE,
                description=self.__config.COMMAND_NOT_FOUND,
                colour=self.__config.COLOURS['black']
            )
            await ctx.send(embed=embed)
        elif isinstance(error, UserInputError):
            my_error = False
            if len(error.args) > 0:
                for arg in error.args:
                    if arg == self.__config.MY_ERROR_BAD_COMMAND:
                        embed = discord.Embed(
                            title=self.__config.BAD_COMMAND_TITLE,
                            description=self.__config.BAD_COMMAND,
                            colour=self.__config.COLOURS['black']
                        )
                        await ctx.send(embed=embed)
                        my_error = True
                        break
            if not my_error:
                raise error
        else:
            print(f'DEVELOPER NOTE -> Comand Error: {error}')
            embed = discord.Embed(
                title=self.__config.ERROR_TITLE,
                description=self.__config.UNKNOWN_ERROR,
                colour=self.__config.COLOURS['red']
            )
            await ctx.send(embed=embed)

    @commands.command(name="help", help=helper.HELP_HELP, description=helper.HELP_HELP_LONG, aliases=['h', 'ajuda'])
    async def help_msg(self, ctx, command_help=''):
        if command_help != '':
            for command in self.__bot.commands:
                if command.name == command_help:
                    txt = command.description if command.description else command.help

                    embedhelp = discord.Embed(
                        title=f'**Description of {command_help}** command',
                        description=txt,
                        colour=self.__config.COLOURS['blue']
                    )

                    await ctx.send(embed=embedhelp)
                    return

            embedhelp = discord.Embed(
                title='Command Help',
                description=f'Command {command_help} Not Found',
                colour=self.__config.COLOURS['red']
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
            helptxt += f'\n\nType {self.__config.BOT_PREFIX}help "command" for more information about the command chosen'
            embedhelp = discord.Embed(
                title=f'**Available Commands of {self.__bot.user.name}**',
                description=helptxt,
                colour=self.__config.COLOURS['blue']
            )

            embedhelp.set_thumbnail(url=self.__bot.user.avatar_url)
            await ctx.send(embed=embedhelp)

    @commands.command(name='invite', help=helper.HELP_INVITE, description=helper.HELP_INVITE_LONG)
    async def invite_bot(self, ctx):
        invite_url = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot>'.format(
            self.__bot.user.id)
        txt = self.__config.INVITE_MESSAGE.format(invite_url)

        embed = discord.Embed(
            title="Invite Vulkan",
            description=txt,
            colour=self.__config.COLOURS['blue']
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Control(bot))
