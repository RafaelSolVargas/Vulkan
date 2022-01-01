import requests
import json
import discord
from discord.ext import commands
from config import config
from discord import Embed


class Warframe(commands.Cog):
    """Deal with the generation of warframe data"""

    def __init__(self, bot: discord.Client):
        self.__bot = bot
        self.__open_functions = ['cetus', 'cambion', 'fissures']

    @commands.command(name='warframe', help=config.HELP_WARFRAME)
    async def warframe(self, ctx, arg) -> Embed:
        if arg in self.__open_functions:
            # Get the required function
            function = getattr(Warframe, f'_Warframe__{arg}')
            embed = await function(self)  # Execute the function passing self

            await ctx.send(embed=embed)  # Return the result
        else:
            info = f'Warframe commands: {self.__open_functions}'

            embed = Embed(
                title='Invalid Command',
                description=info,
                colour=config.COLOURS['blue']
            )
            await ctx.send(embed=embed)

    async def __cetus(self) -> Embed:
        description = await self.__get_cetus()
        embed = discord.Embed(
            title='Warframe Cetus Timing',
            description=description,
            colour=config.COLOURS['blue']
        )
        return embed

    async def __get_cetus(self) -> str:
        """Return the information of the Warframe API"""
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_CETUS_TRIES:
                return 'Os DE baiano não tão com o banco de dados ligado'

            try:
                response = requests.get(config.CETUS_API)
                data = json.loads(response.content)
                short = data['shortString']

                return short

            except Exception as e:
                continue

    async def __cambion(self) -> Embed:
        description = await self.__get_cambion()
        embed = discord.Embed(
            title='Warframe Cambion Timing',
            description=description,
            colour=config.COLOURS['blue']
        )
        return embed

    async def __get_cambion(self) -> str:
        """Return the information of the Warframe API"""
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_CAMBION_TRIES:
                return 'Os DE baiano não tão com o banco de dados ligado'

            try:
                response = requests.get(config.CAMBION_API)
                data = json.loads(response.content)

                info = f'**Active:** {data["active"]}\n**Time Left:** {data["timeLeft"]}'

                return info
            except Exception as e:
                print(e)
                continue

    async def __fissures(self) -> Embed:
        description = await self.__get_fissures()
        embed = discord.Embed(
            title='Warframe Fissures Status',
            description=description,
            colour=config.COLOURS['blue']
        )
        return embed

    async def __get_fissures(self) -> str:
        """Return the information of the Warframe API"""
        tries = 0
        while True:
            tries += 1
            if tries > config.MAX_API_FISSURES_TRIES:
                return 'Os DE baiano não tão com o banco de dados ligado'

            try:
                response = requests.get(config.FISSURES_API)
                data = json.loads(response.content)

                info = ''
                for pos, fissure in enumerate(data, start=1):
                    info += f'`{pos}` - **Mission:** {fissure["missionType"]} | **Type:** {fissure["tier"]} | **Timing:** {fissure["eta"]} | **Storm:** {fissure["isStorm"]}\n'

                return info
            except Exception as e:
                print(e)
                continue


def setup(bot):
    bot.add_cog(Warframe(bot))
