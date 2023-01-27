from asyncio import AbstractEventLoop
from discord import Guild, Status, Game, Message
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from Config.Configs import VConfigs
from discord.ext.commands import Bot, Context
from Config.Messages import Messages
from Config.Embeds import VEmbeds


class VulkanBot(Bot):
    def __init__(self, listingSlash: bool = False, *args, **kwargs):
        """If listing Slash is False then the process is just a Player Process, should not interact with discord commands"""
        super().__init__(*args, **kwargs)
        self.__listingSlash = listingSlash
        self.__configs = VConfigs()
        self.__messages = Messages()
        self.__embeds = VEmbeds()
        self.remove_command("help")

    @property
    def listingSlash(self) -> bool:
        return self.__listingSlash

    def startBot(self) -> None:
        """Blocking function that will start the bot"""
        if self.__configs.BOT_TOKEN == '':
            print('DEVELOPER NOTE -> Token not found')
            exit()

        super().run(self.__configs.BOT_TOKEN, reconnect=True)

    async def startBotCoro(self, loop: AbstractEventLoop) -> None:
        """Start a bot coroutine, does not wait for connection to be established"""
        task = loop.create_task(self.__login())
        await task
        loop.create_task(self.__connect())

    async def __login(self):
        """Coroutine to login the Bot in discord"""
        await self.login(token=self.__configs.BOT_TOKEN)

    async def __connect(self):
        """Coroutine to connect the Bot in discord"""
        await self.connect(reconnect=True)

    async def on_ready(self):
        if self.__listingSlash:
            print(self.__messages.STARTUP_MESSAGE)
        await self.change_presence(status=Status.online, activity=Game(name=f"Vulkan | {self.__configs.BOT_PREFIX}help"))
        if self.__listingSlash:
            print(self.__messages.STARTUP_COMPLETE_MESSAGE)

    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            embed = self.__embeds.MISSING_ARGUMENTS()
            await ctx.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = self.__embeds.COMMAND_NOT_FOUND()
            await ctx.send(embed=embed)

        else:
            print(f'DEVELOPER NOTE -> Command Error: {error}')
            embed = self.__embeds.UNKNOWN_ERROR()
            await ctx.send(embed=embed)

    async def process_commands(self, message: Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=Context)

        if ctx.valid and not message.guild:
            return

        await self.invoke(ctx)


class Context(Context):
    bot: VulkanBot
    guild: Guild
