from random import choices
import string
from discord.bot import Bot
from discord import Intents
from Music.VulkanBot import VulkanBot
from os import listdir
from Config.Configs import VConfigs
from Config.Exceptions import VulkanError


class VulkanInitializer:
    def __init__(self, willListen: bool) -> None:
        self.__config = VConfigs()
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
            bot = VulkanBot(listingSlash=True,
                            command_prefix=prefix,
                            pm_help=True,
                            case_insensitive=True,
                            intents=self.__intents)
        else:
            prefix = ''.join(choices(string.ascii_uppercase + string.digits, k=4))
            bot = VulkanBot(listingSlash=False,
                            command_prefix=prefix,
                            pm_help=True,
                            case_insensitive=True,
                            intents=self.__intents)
        return bot

    def __add_cogs(self, bot: Bot) -> None:
        try:
            cogsStatus = []
            for filename in listdir(self.__config.COMMANDS_PATH):
                if filename.endswith('.py'):
                    cogPath = f'{self.__config.COMMANDS_FOLDER_NAME}.{filename[:-3]}'
                    cogsStatus.append(bot.load_extension(cogPath, store=True))

            if len(bot.cogs.keys()) != self.__getTotalCogs():
                print(cogsStatus)
                raise VulkanError(message='Failed to load some Cog')

        except VulkanError as e:
            print(f'[Error Loading Vulkan]')
            print(e)

    def __getTotalCogs(self) -> int:
        quant = 0
        for filename in listdir(self.__config.COMMANDS_PATH):
            if filename.endswith('.py'):
                quant += 1
        return quant
