from Config.Configs import Singleton


class TestsConstants(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.EMPTY_STRING_ERROR_MSG = 'Downloader with Empty String should be empty list.'
            self.SPOTIFY_TRACK_URL = 'https://open.spotify.com/track/7wpnz7hje4FbnjZuWQtJHP'
            self.MUSIC_TITLE_STRING = 'Experience || AMV || Anime Mix'
            self.YOUTUBE_MUSIC_URL = 'https://www.youtube.com/watch?v=MvJoiv842mk'
