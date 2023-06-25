from discord import Embed
from discord.ext.commands import Cog, command
from Config.Configs import VConfigs
from Config.Helper import Helper
from Config.Colors import VColors
from Music.VulkanBot import VulkanBot
from Config.Embeds import VEmbeds

helper = Helper()


class ControlCog(Cog):
    """Class to handle discord events"""

    def __init__(self, bot: VulkanBot):
        self.__bot = bot
        self.__config = VConfigs()
        self.__colors = VColors()
        self.__embeds = VEmbeds()
        self.__commands = {
            'MUSIC': ['resume', 'pause', 'loop', 'stop',
                      'skip', 'play', 'queue', 'clear',
                      'np', 'shuffle', 'move', 'remove',
                      'reset', 'prev', 'history', 'volume'],
            'RANDOM': ['choose', 'cara', 'random']

        }

    @command(name="help", help=helper.HELP_HELP, description=helper.HELP_HELP_LONG, aliases=['h', 'ajuda'])
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
                title='Help',
                description=f'Command {command_help} do not exists, type {self.__config.BOT_PREFIX}help to see all commands',
                colour=self.__colors.BLACK
            )

            await ctx.send(embed=embedhelp)
        else:

            helptxt = ''
            help_music = '🎧 `MUSIC`\n'
            help_random = '🎲 `RANDOM`\n'
            help_help = '👾 `HELP`\n'

            for command in self.__bot.commands:
                if command.name in self.__commands['MUSIC']:
                    help_music += f'**{command}** - {command.help}\n'

                elif command.name in self.__commands['RANDOM']:
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

            if self.__bot.user.avatar != None:
                embedhelp.set_thumbnail(url=self.__bot.user.avatar)
            await ctx.send(embed=embedhelp)

    @command(name='invite', help=helper.HELP_INVITE, description=helper.HELP_INVITE_LONG, aliases=['convite', 'inv', 'convidar'])
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
    bot.add_cog(ControlCog(bot))
