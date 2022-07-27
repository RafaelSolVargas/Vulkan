from random import choices
import string
from discord.bot import Bot
from discord import Intents
from Music.MusicBot import VulkanBot
from os import listdir
from Config.Configs import Configs


class VulkanInitializer:
    def __init__(self, willListen: bool) -> None:
        self.__config = Configs()
        self.__intents = Intents.default()
        self.__intents.message_content = True
        self.__intents.members = True
        self.__bot = self.__create_bot(willListen)
        self.__add_cogs(self.__bot)

    def getBot(self) -> VulkanBot:
        return self.__bot

    def __create_bot(self, willListen: bool) -> VulkanBot:
        if willListen:
            prefix = self.__config.BOT_PREFIX
        else:
            prefix = ''.join(choices(string.ascii_uppercase + string.digits, k=4))

        bot = VulkanBot(command_prefix=prefix,
                        pm_help=True,
                        case_insensitive=True,
                        intents=self.__intents)
        return bot

    def __add_cogs(self, bot: Bot) -> None:
        try:
            for filename in listdir(f'./{self.__config.COMMANDS_PATH}'):
                if filename.endswith('.py'):
                    print(f'Loading {filename}')
                    bot.load_extension(f'{self.__config.COMMANDS_PATH}.{filename[:-3]}')

            bot.load_extension(f'DiscordCogs.MusicCog')
        except Exception as e:
            print(e)
