from Config.Configs import Singleton


class TestsConstants(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.EMPTY_STRING_ERROR_MSG = 'Downloader with Empty String should be empty list.'
            self.MUSIC_TITLE_STRING = 'Experience || AMV || Anime Mix'

            self.YT_MUSIC_URL = 'https://www.youtube.com/watch?v=MvJoiv842mk'
            self.YT_MIX_URL = 'https://www.youtube.com/watch?v=ePjtnSPFWK8&list=RDMMePjtnSPFWK8&start_radio=1'
            self.YT_PERSONAL_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLbbKJHHZR9ShYuKAr71cLJCFbYE-83vhS'
            # Links from playlists in channels some times must be extracted with force by Downloader
            self.YT_CHANNEL_PLAYLIST_URL = 'https://www.youtube.com/watch?v=MvJoiv842mk&list=PLAI1099Tvk0zWU8X4dwc4vv4MpePQ4DLl'

            self.SPOTIFY_TRACK_URL = 'https://open.spotify.com/track/7wpnz7hje4FbnjZuWQtJHP'
            self.SPOTIFY_PLAYLIST_URL = 'https://open.spotify.com/playlist/37i9dQZF1EIV9u4LtkBkSF'
            self.SPOTIFY_ARTIST_URL = 'https://open.spotify.com/artist/4HF14RSTZQcEafvfPCFEpI'
            self.SPOTIFY_ALBUM_URL = 'https://open.spotify.com/album/71O60S5gIJSIAhdnrDIh3N'
            self.SPOTIFY_WRONG1_URL = 'https://open.spotify.com/wrongUrl'
            self.SPOTIFY_WRONG2_URL = 'https://open.spotify.com/track/WrongID'

            self.DEEZER_TRACK_URL = 'https://www.deezer.com/br/track/33560861'
            self.DEEZER_ARTIST_URL = 'https://www.deezer.com/br/artist/180'
            self.DEEZER_PLAYLIST_URL = 'https://www.deezer.com/br/playlist/1001939451'
            self.DEEZER_ALBUM_URL = 'https://www.deezer.com/en/album/236107012'
            self.DEEZER_WRONG1_URL = 'xxxhttps://www.deezer.com/br/album/5'
            self.DEEZER_WRONG2_URL = 'https://www.deezer.com/en/album/23610701252'
