from dotenv import dotenv_values

CETUS_API = dotenv_values('.env')['CETUS_API']
CAMBION_API = dotenv_values('.env')['CAMBION_API']
FISSURES_API = dotenv_values('.env')['FISSURES_API']
BOT_TOKEN = dotenv_values('.env')['BOT_TOKEN']
SPOTIFY_ID = dotenv_values('.env')['SPOTIFY_ID']
SPOTIFY_SECRET = dotenv_values('.env')['SPOTIFY_SECRET']
SECRET_MESSAGE = dotenv_values('.env')['SECRET_MESSAGE']
PHRASES_API = dotenv_values('.env')['PHRASES_API']

BOT_PREFIX = '!'
INITIAL_EXTENSIONS = {'vulkanbot.commands.Phrases', 'vulkanbot.commands.Warframe',
                      'vulkanbot.general.Filter', 'vulkanbot.general.Control', 'vulkanbot.music.Music',
                      'vulkanbot.commands.Random', 'vulkanbot.general.Admin'}


STARTUP_MESSAGE = 'Starting Vulkan...'
STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'

MAX_PLAYLIST_LENGTH = 50
MAX_API_PHRASES_TRIES = 10
MAX_API_CETUS_TRIES = 10
MAX_API_CAMBION_TRIES = 10
MAX_API_FISSURES_TRIES = 10
MAX_PRELOAD_SONGS = 10

TRASH_CHANNEL_ID = 919961802140450837

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
HELP_WARFRAME = f'({BOT_PREFIX}warframe help for more) - Return warframe information'
HELP_RANDOM = '(x) - Return a random number between 1 and x'
HELP_ESCOLHA = '(x, y, z...) - Choose randomly one item passed in the command'
HELP_CARA = 'Return cara or coroa'
HELP_DROP = '(user_name) - Try to remove the user from the current voice channel'
HELP_FRASE = "Send a randomly phrase, there's a chance of getting the braba"
HELP_HELP = 'This command :)'

ABSOLUTE_PATH = ''
COOKIE_PATH = '/config/cookies/cookies.txt'


COLOURS = {
    'red': 0xDC143C,
    'green': 0x58D68D,
    'grey': 0x708090,
    'blue': 0x3498DB
}

MEMBERS_MAXIMUM_DROPS = {
    'RafaelV': 1,
    'Gassu': 2,
    'LopesZ3R4': 4,
    'BABIGIRL': 4,
    'Hijãomi': 2,
    'Jillian': 4,
    'Maxymuns': 2

}
