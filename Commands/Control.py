from discord import Client, Game, Status, Embed
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, UserInputError
from discord.ext import commands
from Config.Config import Configs
from Config.Helper import Helper
from Config.Messages import Messages
from Config.Colors import Colors
from Views.Embeds import Embeds

helper = Helper()


class Control(commands.Cog):

    def __init__(self, bot: Client):
        self.__bot = bot
        self.__config = Configs()
        self.__messages = Messages()
        self.__colors = Colors()
        self.__embeds = Embeds()
        self.__comandos = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop',
                      'skip', 'play', 'queue', 'clear',
                      'np', 'shuffle', 'move', 'remove',
                      'reset', 'prev', 'history'],
            'RANDOM': ['choose', 'cara', 'random']

        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.__messages.STARTUP_MESSAGE)
        await self.__bot.change_presence(status=Status.online, activity=Game(name=f"Vulkan | {self.__config.BOT_PREFIX}help"))
        print(self.__messages.STARTUP_COMPLETE_MESSAGE)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = self.__embeds.MISSING_ARGUMENTS()
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = self.__embeds.COMMAND_NOT_FOUND()
            await ctx.send(embed=embed)

        else:
            print(f'DEVELOPER NOTE -> Comand Error: {error}')
            embed = self.__embeds.UNKNOWN_ERROR()
            await ctx.send(embed=embed)

    @commands.command(name="help", help=helper.HELP_HELP, description=helper.HELP_HELP_LONG, aliases=['h', 'ajuda'])
    async def help_msg(self, ctx, command_help=''):
        if command_help != '':
            for command in self.__bot.commands:
                if command.name == command_help:
                    txt = command.description if command.description else command.help

                    embedhelp = Embed(
                        title=f'**Description of {command_help}** command',
                        description=txt,
                        colour=self.__colors.BLUE
                    )

                    await ctx.send(embed=embedhelp)
                    return

            embedhelp = Embed(
                title='Command Help',
                description=f'Command {command_help} Not Found',
                colour=self.__colors.RED
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
            embedhelp = Embed(
                title=f'**Available Commands of {self.__bot.user.name}**',
                description=helptxt,
                colour=self.__colors.BLUE
            )

            embedhelp.set_thumbnail(url=self.__bot.user.avatar_url)
            await ctx.send(embed=embedhelp)

    @commands.command(name='invite', help=helper.HELP_INVITE, description=helper.HELP_INVITE_LONG)
    async def invite_bot(self, ctx):
        invite_url = self.__config.INVITE_URL.format(self.__bot.user.id)
        txt = self.__config.INVITE_MESSAGE.format(invite_url, invite_url)

        embed = Embed(
            title="Invite Vulkan",
            description=txt,
            colour=self.__colors.BLUE
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Control(bot))
