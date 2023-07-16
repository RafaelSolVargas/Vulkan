from Config.Singleton import Singleton
from Config.Configs import VConfigs


class Helper(Singleton):
    def __init__(self) -> None:
        if not super().created:
            config = VConfigs()
            self.HELP_SKIP = 'Skip the current playing song.'
            self.HELP_SKIP_LONG = 'Skip the playing of the current song, does not work if loop one is activated. \n\nArguments: None.'
            self.HELP_RESUME = 'Resumes the song player.'
            self.HELP_RESUME_LONG = 'If the player if paused, return the playing. \n\nArguments: None.'
            self.HELP_CLEAR = 'Clear the queue and songs history.'
            self.HELP_CLEAR_LONG = 'Clear the songs queue and songs history. \n\nArguments: None.'
            self.HELP_STOP = 'Stop the song player.'
            self.HELP_STOP_LONG = 'Stop the song player, clear queue and history and remove Vulkan from voice channel.\n\nArguments: None.'
            self.HELP_LOOP = 'Control the loop of songs.'
            self.HELP_LOOP_LONG = """Control the loop of songs.\n\n Require: A song being played.\nArguments:
                One - Start looping the current song.
                All - Start looping all songs in queue.
                Off - Disable loop."""
            self.HELP_NP = 'Show the info of the current song.'
            self.HELP_NP_LONG = 'Show the information of the song being played.\n\nRequire: A song being played.\nArguments: None.'
            self.HELP_QUEUE = f'Show the first {config.MAX_SONGS_IN_PAGE} songs in queue.'
            self.HELP_QUEUE_LONG = f'Show the first {config.MAX_SONGS_IN_PAGE} song in the queue.\n\nArguments: None.'
            self.HELP_PAUSE = 'Pauses the song player.'
            self.HELP_PAUSE_LONG = 'If playing, pauses the song player.\n\nArguments: None'
            self.HELP_PREV = 'Play the previous song.'
            self.HELP_PREV_LONG = 'Play the previous song. If playing, the current song will return to queue.\n\nRequire: Loop to be disable.\nArguments: None.'
            self.HELP_SHUFFLE = 'Shuffle the songs playing.'
            self.HELP_SHUFFLE_LONG = 'Randomly shuffle the songs in the queue.\n\nArguments: None.'
            self.HELP_PLAY = 'Plays a song from URL.'
            self.CHANGE_VOLUME = 'Set the volume of the song.'
            self.CHANGE_VOLUME_LONG = 'Change the volume of the song, expect a number from 0 to 100.'
            self.HELP_PLAY_LONG = 'Play a song in discord. \n\nRequire: You to be connected to a voice channel.\nArguments: Youtube, Spotify or Deezer song/playlist link or the title of the song to be searched in Youtube.'
            self.HELP_HISTORY = f'Show the history of played songs.'
            self.HELP_HISTORY_LONG = f'Show the last {config.MAX_SONGS_HISTORY} played songs'
            self.HELP_MOVE = 'Moves a song from position pos1 to pos2 in queue.'
            self.HELP_MOVE_LONG = 'Moves a song from position x to position y in queue.\n\nRequire: Positions to be both valid numbers.\nArguments: 1º Number => Initial position, 2º Number => Destination position. Both numbers could be -1 to refer to the last song in queue.\nDefault: By default, if the second number is not passed, it will be 1, moving the selected song to 1º position.'
            self.HELP_REMOVE = 'Remove a song in position x.'
            self.HELP_REMOVE_LONG = 'Remove a song from queue in the position passed.\n\nRequire: Position to be a valid number.\nArguments: 1º          self.Number => Position in queue of the song.'
            self.HELP_RESET = 'Reset the Player of the server.'
            self.HELP_RESET_LONG = 'Reset the Player of the server. Recommended if you find any type of error.\n\nArguments: None'
            self.HELP_HELP = f'Use {config.BOT_PREFIX}help "command" for more info.'
            self.HELP_HELP_LONG = f'Use {config.BOT_PREFIX}help command for more info about the command selected.'
            self.HELP_INVITE = 'Send the invite URL to call Vulkan to your server.'
            self.HELP_INVITE_LONG = 'Send an message in text channel with a URL to be used to invite Vulkan to your own server.\n\nArguments: None.'
            self.HELP_RANDOM = 'Return a random number between 1 and x.'
            self.HELP_RANDOM_LONG = 'Send a randomly selected number between 1 and the number you pass.\n\nRequired: Number to be a valid number.\nArguments: 1º Any number to be used as range.'
            self.HELP_CHOOSE = 'Choose randomly one item passed.'
            self.HELP_CHOOSE_LONG = 'Choose randomly one item passed in this command.\n\nRequire: Itens to be separated by comma.\nArguments: As much as you want.'
            self.HELP_CARA = 'Return cara or coroa.'
            self.HELP_CARA_LONG = 'Return cara or coroa.'

            self.SLASH_QUEUE_DESCRIPTION = f'Number of queue page, there is only {config.MAX_SONGS_IN_PAGE} musics by page'
            self.SLASH_MOVE_HELP = 'Moves a song from position pos1 to pos2 in queue.'
