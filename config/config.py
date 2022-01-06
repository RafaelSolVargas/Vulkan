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

STARTUP_MESSAGE = 'Starting Vulkan...'
STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'

MAX_PLAYLIST_LENGTH = 50
MAX_API_PHRASES_TRIES = 10
MAX_API_CETUS_TRIES = 10
MAX_API_CAMBION_TRIES = 10
MAX_API_FISSURES_TRIES = 10
MAX_PRELOAD_SONGS = 10

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "

HELP_SKIP = 'Skip the current playing song'
HELP_RESUME = 'Resumes the song player'
HELP_CLEAR = 'Clear the queue'
HELP_STOP = 'Stop the song player, removing Vulkan from voice channel'
HELP_LOOP = '(one/all/off) - Control the loop of songs'
HELP_NP = 'Show the info of the current song'
HELP_QUEUE = f'Show the first {MAX_PRELOAD_SONGS} songs in queue'
HELP_PAUSE = 'Pauses the song player'
HELP_SHUFFLE = 'Shuffle the songs playing'
HELP_PLAY = '(title/youtube/spotify) - Plays a song'
HELP_MOVE = '(x, y) - Moves a song from position x to y in queue'
HELP_REMOVE = '(x, -1) - Remove a song in the position x or -1 for the last song'
HELP_RESET = 'Reset the Player of a guild'
HELP_WARFRAME = f'({BOT_PREFIX}warframe help for more)'
HELP_RANDOM = '(x) - Return a random number between 1 and x'
HELP_ESCOLHA = '(x, y, z...) - Choose randomly one item passed'
HELP_CARA = 'Return cara or coroa'
HELP_DROP = '(user_name) - Try to remove the user from the current voice channel'
HELP_FRASE = "Send a randomly phrase, perhaps you get the braba"
HELP_HELP = 'This command :)'

NO_CHANNEL = 'To play some music, connect to any voice channel first.'
INVALID_INPUT = 'This type of input was too strange, try something better'
DOWNLOADING_ERROR = 'An error occurred while downloading'
SONG_ADDED = 'Song added to the Queue'

COLOURS = {
    'red': 0xDC143C,
    'green': 0x58D68D,
    'grey': 0x708090,
    'blue': 0x3498DB
}
