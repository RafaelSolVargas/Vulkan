from decouple import config

CETUS_API = config('CETUS_API')
CAMBION_API = config('CAMBION_API')
FISSURES_API = config('FISSURES_API')
BOT_TOKEN = config('BOT_TOKEN')
SPOTIFY_ID = config('SPOTIFY_ID')
SPOTIFY_SECRET = config('SPOTIFY_SECRET')
SECRET_MESSAGE = config('SECRET_MESSAGE')
PHRASES_API = config('PHRASES_API')

BOT_PREFIX = '!'
VC_TIMEOUT = 600

STARTUP_MESSAGE = 'Starting Vulkan...'
STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

MAX_PLAYLIST_LENGTH = 50
MAX_API_PHRASES_TRIES = 10
MAX_API_CETUS_TRIES = 10
MAX_API_CAMBION_TRIES = 10
MAX_API_FISSURES_TRIES = 10
MAX_PRELOAD_SONGS = 10

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_REQUESTER = 'Requester: '

HELP_SKIP = 'Skip the current playing song.'
HELP_RESUME = 'Resumes the song player.'
HELP_CLEAR = 'Clear the queue.'
HELP_STOP = 'Stop the song player, removing Vulkan from voice channel.'
HELP_LOOP = '(one/all/off) - Control the loop of songs.'
HELP_NP = 'Show the info of the current song.'
HELP_QUEUE = f'Show the first {MAX_PRELOAD_SONGS} songs in queue.'
HELP_PAUSE = 'Pauses the song player.'
HELP_SHUFFLE = 'Shuffle the songs playing.'
HELP_PLAY = '(title/youtube/spotify) - Plays a song.'
HELP_MOVE = '(x, y) - Moves a song from position x to y in queue.'
HELP_REMOVE = '(x, -1) - Remove a song in the position x or -1 for the last song.'
HELP_RESET = 'Reset the Player of a server.'
HELP_WARFRAME = f'({BOT_PREFIX}warframe help for more).'
HELP_RANDOM = '(x) - Return a random number between 1 and x.'
HELP_ESCOLHA = '(x, y, z...) - Choose randomly one item passed.'
HELP_CARA = 'Return cara or coroa.'
HELP_DROP = '(user_name) - Try to remove the user from the current voice channel.'
HELP_FRASE = "Send a randomly phrase, perhaps you get the secret."
HELP_HELP = 'This command :)'
HELP_LONG_LOOP = 'Loop Command Help\nOne - Start looping the current song\nAll - Start looping all songs in queue\nOff - Disable the song loop'

SONGS_ADDED = 'You added {} songs to the queue'
SONG_ADDED = 'You added the song {} to the queue'
SONG_ADDED_TWO = '🎧 Song added to the queue'
SONG_PLAYING = '🎧 Song playing now'
SONG_PLAYER = '🎧 Song Player'
QUEUE_TITLE = '🎧 Songs in Queue'
ONE_SONG_LOOPING = '🎧 Looping One Song'
ALL_SONGS_LOOPING = '🎧 Looping All Songs'
SONG_PAUSED = '⏸️ Song paused'
SONG_RESUMED = '▶️ Song playing'
EMPTY_QUEUE = f'❌ Song queue is empty, use {BOT_PREFIX}play to add new songs'
SONG_DOWNLOADING = '📥 Downloading...'

SONGS_SHUFFLED = '🔀 Songs shuffled successfully'
ERROR_SHUFFLING = '❌ Error while shuffling the songs'
ERROR_MOVING = '❌ Error while moving the songs'
LENGTH_ERROR = '❌ Numbers must be between 1 and queue length, use -1 for the last song'
ERROR_NUMBER = '❌ This command require a number'
ERROR_PLAYING = '❌ Error while playing songs'
COMMAND_NOT_FOUND = f'❌ Command not found, type {BOT_PREFIX}help to see all commands'
UNKNOWN_ERROR = '❌ Unknown Error'
ERROR_MISSING_ARGUMENTS = f'❌ Missing arguments in this function. Type {BOT_PREFIX}help to see all commands'
ERROR_WHILE_REQUESTING = 'O banco de dados dos cara tá off, bando de vagabundo, tenta depois aí bicho'

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

SONGS_PLAYING_TITLES = [ONE_SONG_LOOPING, ALL_SONGS_LOOPING, SONG_PLAYING]

ERROR_TITLE = 'Error :-('
NO_CHANNEL = 'To play some music, connect to any voice channel first.'
NO_GUILD = f'This server are not connected to Vulkan, try {BOT_PREFIX}reset'
INVALID_INPUT = 'This type of input was too strange, try something better'
DOWNLOADING_ERROR = 'An error occurred while downloading'
EXTRACTING_ERROR = 'An error ocurred while searching for the songs'

COLOURS = {
    'red': 0xDC143C,
    'green': 0x58D68D,
    'grey': 0x708090,
    'blue': 0x3498DB
}
