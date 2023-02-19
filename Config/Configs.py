from decouple import config
from Config.Singleton import Singleton
from Config.Folder import Folder


class VConfigs(Singleton):
    def __init__(self) -> None:
        if not super().created:
            # You can change this boolean to False if you want to prevent the Bot from auto disconnecting
            # Resolution for the issue: https://github.com/RafaelSolVargas/Vulkan/issues/33
            self.SHOULD_AUTO_DISCONNECT_WHEN_ALONE = False
            # Recommended to be True, except in cases when your Bot is present in thousands servers, in that case
            # the delay to start a new Python process for the playback is too much, and to avoid that you set as False
            self.SONG_PLAYBACK_IN_SEPARATE_PROCESS = False

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
            self.QUEUE_VIEW_TIMEOUT = 120
            self.COMMANDS_FOLDER_NAME = 'DiscordCogs'
            self.COMMANDS_PATH = f'{Folder().rootFolder}{self.COMMANDS_FOLDER_NAME}'
            self.VC_TIMEOUT = 300

            self.CHANCE_SHOW_PROJECT = 15
            self.PROJECT_URL = 'https://github.com/RafaelSolVargas/Vulkan'
            self.SUPPORTING_ICON = 'https://i.pinimg.com/originals/d6/05/b4/d605b4f8c5d1c6ae20dc353ef9f091bd.png'

            self.MAX_PLAYLIST_LENGTH = 50
            self.MAX_PLAYLIST_FORCED_LENGTH = 5
            self.MAX_SONGS_IN_PAGE = 10
            self.MAX_PRELOAD_SONGS = 15
            self.MAX_SONGS_HISTORY = 15

            self.INVITE_MESSAGE = """To invite Vulkan to your own server, click [here]({}). 
            Or use this direct URL: {}"""

            self.MY_ERROR_BAD_COMMAND = 'This string serves to verify if some error was raised by myself on purpose'
            self.INVITE_URL = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'

    def getPlayersManager(self):
        return self.__manager

    def setPlayersManager(self, newManager):
        self.__manager = newManager
