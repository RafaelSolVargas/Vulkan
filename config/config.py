from dotenv import dotenv_values

CETUS_API = dotenv_values('.env')['CETUS_API']
BOT_TOKEN = dotenv_values('.env')['BOT_TOKEN']
SPOTIFY_ID = dotenv_values('.env')['SPOTIFY_ID']
SPOTIFY_SECRET = dotenv_values('.env')['SPOTIFY_SECRET']
SECRET_MESSAGE = dotenv_values('.env')['SECRET_MESSAGE']
PHRASES_API = dotenv_values('.env')['PHRASES_API']

BOT_PREFIX = '!'
INITIAL_EXTENSIONS = {'vulkanbot.commands.Phrases', 'vulkanbot.commands.Warframe',
                      'vulkanbot.general.Filter', 'vulkanbot.general.Control', 'vulkanbot.music.Music',
                      'vulkanbot.commands.Random'}

VC_TIMEOUT = 600  # seconds
VC_TIMEOUT_DEFAULT = True

STARTUP_MESSAGE = 'Starting Vulkan...'
STARTUP_COMPLETE_MESSAGE = 'Vulkan is now operating.'

USER_NOT_IN_VC_MESSAGE = "Error: Please join the active voice channel to use this command"
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
ALREADY_CONNECTED_MESSAGE = "Error: Already connected to a voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel"

INFO_HISTORY_TITLE = "Songs Played:"
MAX_HISTORY_LENGTH = 10
MAX_PLAYLIST_LENGTH = 50
MAX_QUEUE_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15
MAX_API_PHRASES_TRIES = 10
MAX_API_CETUS_TRIES = 10

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "
SONGINFO_NOW_PLAYING = "Now Playing"
SONGINFO_QUEUE_ADDED = "Added to queue"
SONGINFO_SONGINFO = "Song info"
SONGINFO_PLAYLIST_QUEUED = "Queued playlist :page_with_curl:"
SONGINFO_UNKNOWN_DURATION = "Unknown"


HELP_HISTORY_LONG = "Shows the " + \
    str(MAX_TRACKNAME_HISTORY_LENGTH) + " last played songs."
HELP_PAUSE_LONG = "Pauses the AudioPlayer. Playback can be continued with the resume command."
HELP_VOL_LONG = "Changes the volume of the AudioPlayer. Argument specifies the % to which the volume should be set."
HELP_PREV_LONG = "Plays the previous song again."
HELP_RESUME_LONG = "Resumes the AudioPlayer."
HELP_SKIP_LONG = "Skips the currently playing song and goes to the next item in the queue."
HELP_SONGINFO_LONG = "Shows details about the song currently being played and posts a link to the song."
HELP_STOP_LONG = "Stops the AudioPlayer and clears the songqueue"
HELP_YT_LONG = (
    "$p [link/video title/key words/playlist-link/soundcloud link/spotify link/bandcamp link/twitter link]")
HELP_CLEAR_LONG = "Clears the queue."
HELP_LOOP_LONG = "Loops the currently playing song and locks the queue. Use the command again to disable loop."
HELP_QUEUE_LONG = "Shows the number of songs in queue, up to 10."
HELP_SHUFFLE_LONG = "Randomly sort the songs in the current queue"

ABSOLUTE_PATH = ''
COOKIE_PATH = '/config/cookies/cookies.txt'


COLOURS = {
    'red': 0xDC143C,
    'green': 0x58D68D,
    'grey': 0x708090,
    'blue': 0x3498DB
}
