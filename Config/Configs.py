from decouple import config
from Config.Singleton import Singleton


class VConfigs(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.BOT_PREFIX = '!'
            try:
                self.BOT_TOKEN = config('BOT_TOKEN')
                self.SPOTIFY_ID = config('SPOTIFY_ID')
                self.SPOTIFY_SECRET = config('SPOTIFY_SECRET')
                self.BOT_PREFIX = config('BOT_PREFIX')
            except:
                print(
                    '[ERROR] -> You must create and .env file with all required fields, see documentation for help')

            self.CLEANER_MESSAGES_QUANT = 5
            self.ACQUIRE_LOCK_TIMEOUT = 10
            self.COMMANDS_PATH = 'DiscordCogs'
            self.VC_TIMEOUT = 600

            self.MAX_PLAYLIST_LENGTH = 50
            self.MAX_PLAYLIST_FORCED_LENGTH = 5
            self.MAX_PRELOAD_SONGS = 15
            self.MAX_SONGS_HISTORY = 15

            self.INVITE_MESSAGE = """To invite Vulkan to your own server, click [here]({}). 
            Or use this direct URL: {}"""

            self.MY_ERROR_BAD_COMMAND = 'This string serves to verify if some error was raised by myself on purpose'
            self.INVITE_URL = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'
