from discord import Intents, Client
from os import listdir
from Config.Configs import Configs
from discord.ext.commands import Bot


class VulkanInitializer:
    def __init__(self) -> None:
        self.__config = Configs()
        self.__intents = Intents.default()
        self.__intents.members = True
        self.__bot = self.__create_bot()
        self.__add_cogs(self.__bot)

    def __create_bot(self) -> Client:
        bot = Bot(command_prefix=self.__config.BOT_PREFIX,
                  pm_help=True,
                  case_insensitive=True,
                  intents=self.__intents)
        bot.remove_command('help')
        return bot

    def __add_cogs(self, bot: Client) -> None:
        for filename in listdir(f'./{self.__config.COMMANDS_PATH}'):
            if filename.endswith('.py'):
                bot.load_extension(f'{self.__config.COMMANDS_PATH}.{filename[:-3]}')

    def run(self) -> None:
        if self.__config.BOT_TOKEN == '':
            print('DEVELOPER NOTE -> Token not found')
            exit()

        self.__bot.run(self.__config.BOT_TOKEN, bot=True, reconnect=True)


vulkan = VulkanInitializer()
vulkan.run()
