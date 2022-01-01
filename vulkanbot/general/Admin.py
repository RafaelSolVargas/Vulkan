from discord.ext import commands
from discord import Member, Client
from config import config


class Admin(commands.Cog):
    """Deal with administration of users in server"""

    def __init__(self, bot: Client):
        self.__bot = bot

    @commands.command(name='drop', help='Manda um membro para a Terapia')
    async def drop(self, ctx, name):
        user: Member = None
        guild = ctx.guild

        for member in guild.members:
            if member.name == name:
                user = member
                break

        if user == None:
            await ctx.send(f'{name} não foi encontrado, utilize o nome de usuário ao invés do apelido do servidor')
            return

        permanent_drops = False
        maximum_drops = None

        try:
            maximum_drops = config.MEMBERS_MAXIMUM_DROPS[user.name]
        except KeyError:
            permanent_drops = True
        except Exception as e:
            await ctx.send('Houve algum erro :/')
            return

        if maximum_drops == 0:
            await ctx.send(f'{user.name} já foi dropado várias vezes, larga o cara bicho')
            return

        if user.voice == None:
            await ctx.send(f'{user.name} precisa estar conectado a um canal de voz antes')
        else:
            await user.move_to(None)  # Remove from voice
            if not permanent_drops:
                # Att the life of user
                config.MEMBERS_MAXIMUM_DROPS[user.name] -= 1


def setup(bot):
    bot.add_cog(Admin(bot))
