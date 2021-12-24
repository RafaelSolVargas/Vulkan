from discord.ext import commands


class Filter(commands.Cog):
    """Deal with filtering of discord messages"""

    def __init__(self, bot):
        self.__bot = bot

    @property
    def bot(self):
        return self.__bot

    @bot.setter
    def bot(self, newBot):
        self.__bot = newBot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.__bot.user:
            return

        if 'elx' in message.content:
            await message.channel.send(f'Coé {message.author.name}, tu é gay memo hein bicho')


def setup(bot):
    bot.add_cog(Filter(bot))
