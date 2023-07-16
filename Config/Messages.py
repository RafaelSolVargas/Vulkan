from Config.Singleton import Singleton
from Config.Configs import VConfigs
from Config.Emojis import VEmojis


class Messages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__emojis = VEmojis()
            configs = VConfigs()
            self.STARTUP_MESSAGE = 'Starting Vulkan...'
            self.STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

            self.SONGINFO_UPLOADER = "Uploader: "
            self.SONGINFO_DURATION = "Duration: "
            self.SONGINFO_REQUESTER = 'Requester: '
            self.SONGINFO_POSITION = 'Position: '

            self.VOLUME_CHANGED = 'Song volume changed to `{}`%'
            self.SONGS_ADDED = 'Downloading `{}` songs to add to the queue'
            self.SONG_ADDED = 'Downloading the song `{}` to add to the queue'
            self.SONG_ADDED_TWO = f'{self.__emojis.MUSIC} Song added to the queue'
            self.SONG_PLAYING = f'{self.__emojis.MUSIC} Song playing now'
            self.SONG_PLAYER = f'{self.__emojis.MUSIC} Song Player'
            self.QUEUE_TITLE = f'{self.__emojis.MUSIC} Songs in Queue'
            self.ONE_SONG_LOOPING = f'{self.__emojis.MUSIC} Looping One Song'
            self.ALL_SONGS_LOOPING = f'{self.__emojis.MUSIC} Looping All Songs'
            self.SONG_PAUSED = f'{self.__emojis.PAUSE} Song paused'
            self.SONG_RESUMED = f'{self.__emojis.PLAY} Song playing'
            self.SONG_SKIPPED = f'{self.__emojis.SKIP} Song skipped'
            self.RETURNING_SONG = f'{self.__emojis.BACK} Playing previous song'
            self.STOPPING = f'{self.__emojis.STOP} Player Stopped'
            self.EMPTY_QUEUE = f'{self.__emojis.QUEUE} Song queue is empty, use {configs.BOT_PREFIX}play to add new songs'
            self.SONG_DOWNLOADING = f'{self.__emojis.DOWNLOADING} Downloading...'
            self.PLAYLIST_CLEAR = f'{self.__emojis.MUSIC} Playlist is now empty'

            self.HISTORY_TITLE = f'{self.__emojis.MUSIC} Played Songs'
            self.HISTORY_EMPTY = f'{self.__emojis.QUEUE} There is no musics in history'

            self.SONG_MOVED_SUCCESSFULLY = 'Song `{}` in position `{}` moved to the position `{}` successfully'
            self.SONG_REMOVED_SUCCESSFULLY = 'Song `{}` removed successfully'

            self.LOOP_ALL_ON = f'{self.__emojis.ERROR} Vulkan is looping all songs, use {configs.BOT_PREFIX}loop off to disable this loop first'
            self.LOOP_ONE_ON = f'{self.__emojis.ERROR} Vulkan is looping one song, use {configs.BOT_PREFIX}loop off to disable this loop first'
            self.LOOP_ALL_ALREADY_ON = f'{self.__emojis.LOOP_ALL} Vulkan is already looping all songs'
            self.LOOP_ONE_ALREADY_ON = f'{self.__emojis.LOOP_ONE} Vulkan is already looping the current song'
            self.LOOP_ALL_ACTIVATE = f'{self.__emojis.LOOP_ALL} Looping all songs'
            self.LOOP_ONE_ACTIVATE = f'{self.__emojis.LOOP_ONE} Looping the current song'
            self.LOOP_DISABLE = f'{self.__emojis.LOOP_OFF} Loop disabled'
            self.LOOP_ALREADY_DISABLE = f'{self.__emojis.ERROR} Loop is already disabled'
            self.LOOP_ON = f'{self.__emojis.ERROR} This command cannot be invoked with any loop activated. Use {configs.BOT_PREFIX}loop off to disable loop'
            self.BAD_USE_OF_LOOP = f"""{self.__emojis.ERROR} Invalid arguments of Loop command. Use {configs.BOT_PREFIX}help loop to more information.
                                -> Available Arguments: ["all", "off", "one", ""]"""

            self.SONGS_SHUFFLED = f'{self.__emojis.SHUFFLE} Songs shuffled successfully'
            self.ERROR_SHUFFLING = f'{self.__emojis.ERROR} Error while shuffling the songs'
            self.ERROR_MOVING = f'{self.__emojis.ERROR} Error while moving the songs'
            self.LENGTH_ERROR = f'{self.__emojis.ERROR} Numbers must be between 1 and queue length, use -1 for the last song'
            self.ERROR_NUMBER = f'{self.__emojis.ERROR} This command require a number'
            self.ERROR_VOLUME_NUMBER = f'{self.__emojis.ERROR} This command require a number between 0 and 100'
            self.ERROR_PLAYING = f'{self.__emojis.ERROR} Error while playing songs'
            self.COMMAND_NOT_FOUND = f'{self.__emojis.ERROR} Command not found, type {configs.BOT_PREFIX}help to see all commands'
            self.UNKNOWN_ERROR = f'{self.__emojis.ERROR} Unknown Error, if needed, use {configs.BOT_PREFIX}reset to reset the player of your server'
            self.ERROR_MISSING_ARGUMENTS = f'{self.__emojis.ERROR} Missing arguments in this command. Type {configs.BOT_PREFIX}help "command" to see more info about this command'
            self.NOT_PREVIOUS = f'{self.__emojis.ERROR} There is none previous song to play'
            self.PLAYER_NOT_PLAYING = f'{self.__emojis.ERROR} No song playing. Use {configs.BOT_PREFIX}play to start the player'
            self.IMPOSSIBLE_MOVE = 'That is impossible :('
            self.ERROR_TITLE = 'Error :-('
            self.COMMAND_NOT_FOUND_TITLE = 'This is strange :-('
            self.NO_CHANNEL = 'To play some music, connect to any voice channel first.'
            self.NO_GUILD = f'This server does not has a Player, try {configs.BOT_PREFIX}reset'
            self.INVALID_INPUT = f'This URL was too strange, try something better or type {configs.BOT_PREFIX}help play'
            self.INVALID_INDEX = f'Invalid index passed as argument.'
            self.INVALID_ARGUMENTS = f'Invalid arguments passed to command.'
            self.DOWNLOADING_ERROR = f"{self.__emojis.ERROR} It's impossible to download and play this video"
            self.EXTRACTING_ERROR = f'{self.__emojis.ERROR} An error ocurred while searching for the songs'

            self.ERROR_IN_PROCESS = f"{self.__emojis.ERROR} Due to a internal error your player was restarted, skipping the song."
            self.MY_ERROR_BAD_COMMAND = 'This string serves to verify if some error was raised by myself on purpose'
            self.BAD_COMMAND_TITLE = 'Misuse of command'
            self.BAD_COMMAND = f'{self.__emojis.ERROR} Bad usage of this command, type {configs.BOT_PREFIX}help "command" to understand the command better'
            self.VIDEO_UNAVAILABLE = f'{self.__emojis.ERROR} Sorry. This video is unavailable for download.'
            self.ERROR_DUE_LOOP_ONE_ON = f'{self.__emojis.ERROR} This command cannot be executed with loop one activated. Use {configs.BOT_PREFIX}loop off to disable loop.'


class SearchMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            config = VConfigs()
            self.UNKNOWN_INPUT = f'This type of input was too strange, try something else or type {config.BOT_PREFIX}help play'
            self.UNKNOWN_INPUT_TITLE = 'Nothing Found'
            self.GENERIC_TITLE = 'URL could not be processed'
            self.SPOTIFY_NOT_FOUND = 'Spotify could not process any songs with this input, verify your link or try again later.'
            self.YOUTUBE_NOT_FOUND = 'Youtube could not process any songs with this input, verify your link or try again later.'
            self.DEEZER_NOT_FOUND = 'Deezer could not process any songs with this input, verify your link or try again later.'


class SpotifyMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.INVALID_SPOTIFY_URL = 'Invalid Spotify URL, verify your link.'
            self.GENERIC_TITLE = 'URL could not be processed'


class DeezerMessages(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.INVALID_DEEZER_URL = 'Invalid Deezer URL, verify your link.'
            self.GENERIC_TITLE = 'URL could not be processed'
