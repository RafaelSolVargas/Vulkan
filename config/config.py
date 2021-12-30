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
                      'vulkanbot.commands.Random'}


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

ABSOLUTE_PATH = ''
COOKIE_PATH = '/config/cookies/cookies.txt'


COLOURS = {
    'red': 0xDC143C,
    'green': 0x58D68D,
    'grey': 0x708090,
    'blue': 0x3498DB
}
