from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
SPOTIFY_ID = config('SPOTIFY_ID')
SPOTIFY_SECRET = config('SPOTIFY_SECRET')

BOT_PREFIX = '!'
VC_TIMEOUT = 600

STARTUP_MESSAGE = 'Starting Vulkan...'
STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

MAX_PLAYLIST_LENGTH = 50
MAX_PRELOAD_SONGS = 10
MAX_SONGS_HISTORY = 15

INVITE_MESSAGE = 'To invite Vulkan to your own server, click [here]({})'

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_REQUESTER = 'Requester: '

SONGS_ADDED = 'You added {} songs to the queue'
SONG_ADDED = 'You added the song `{}` to the queue'
SONG_ADDED_TWO = '🎧 Song added to the queue'
SONG_PLAYING = '🎧 Song playing now'
SONG_PLAYER = '🎧 Song Player'
QUEUE_TITLE = '🎧 Songs in Queue'
ONE_SONG_LOOPING = '🎧 Looping One Song'
ALL_SONGS_LOOPING = '🎧 Looping All Songs'
SONG_PAUSED = '⏸️ Song paused'
SONG_RESUMED = '▶️ Song playing'
EMPTY_QUEUE = f'📜 Song queue is empty, use {BOT_PREFIX}play to add new songs'
SONG_DOWNLOADING = '📥 Downloading...'

HISTORY_TITLE = '🎧 Played Songs'
HISTORY_EMPTY = '📜 There is no musics in history'

SONG_MOVED_SUCCESSFULLY = 'Song `{}` in position `{}` moved with `{}` in position `{}` successfully'
SONG_REMOVED_SUCCESSFULLY = 'Song `{}` removed successfully'

LOOP_ALL_ON = f'❌ Vulkan is looping all songs, use {BOT_PREFIX}loop off to disable this loop first'
LOOP_ONE_ON = f'❌ Vulkan is looping one song, use {BOT_PREFIX}loop off to disable this loop first'
LOOP_ALL_ALREADY_ON = '🔁 Vulkan is already looping all songs'
LOOP_ONE_ALREADY_ON = '🔂 Vulkan is already looping the current song'
LOOP_ALL_ACTIVATE = '🔁 Looping all songs'
LOOP_ONE_ACTIVATE = '🔂 Looping the current song'
LOOP_DISABLE = '➡️ Loop disabled'
LOOP_ALREADY_DISABLE = '❌ Loop is already disabled'
LOOP_ON = f'❌ This command cannot be invoked with any loop activated. Use {BOT_PREFIX}loop off to disable loop'

SONGS_SHUFFLED = '🔀 Songs shuffled successfully'
ERROR_SHUFFLING = '❌ Error while shuffling the songs'
ERROR_MOVING = '❌ Error while moving the songs'
LENGTH_ERROR = '❌ Numbers must be between 1 and queue length, use -1 for the last song'
ERROR_NUMBER = '❌ This command require a number'
ERROR_PLAYING = '❌ Error while playing songs'
COMMAND_NOT_FOUND = f'❌ Command not found, type {BOT_PREFIX}help to see all commands'
UNKNOWN_ERROR = f'❌ Unknown Error, if needed, use {BOT_PREFIX}reset to reset the player of your server'
ERROR_MISSING_ARGUMENTS = f'❌ Missing arguments in this command. Type {BOT_PREFIX}help "command" to see more info about this command'
NOT_PREVIOUS = '❌ There is none previous song to play'
PLAYER_NOT_PLAYING = f'❌ No song playing. Use {BOT_PREFIX}play to start the player'
IMPOSSIBLE_MOVE = 'That is impossible :('
ERROR_TITLE = 'Error :-('
NO_CHANNEL = 'To play some music, connect to any voice channel first.'
NO_GUILD = f'This server does not has a Player, try {BOT_PREFIX}reset'
INVALID_INPUT = f'This type of input was too strange, try something better or type {BOT_PREFIX}help play'
DOWNLOADING_ERROR = '❌ An error occurred while downloading'
EXTRACTING_ERROR = '❌ An error ocurred while searching for the songs'

BAD_COMMAND_TITLE = 'Misuse of command'
BAD_COMMAND = f'❌ Bad usage of this command, type {BOT_PREFIX}help "command" to understand the command better'

COLOURS = {
    'red': 0xDC143C,
    'green': 0x1F8B4C,
    'grey': 0x708090,
    'blue': 0x206694,
    'black': 0x23272A
}
