from discord.ext import commands


class Talks(commands.Cog):
    """Deal with talks to users"""

    def __init__(self, bot):
        self.__bot = bot

    @property
    def bot(self):
        return self.__bot

    @bot.setter
    def bot(self, newBot):
        self.__bot = newBot


def setup(bot):
    bot.add_cog(Talks(bot))
