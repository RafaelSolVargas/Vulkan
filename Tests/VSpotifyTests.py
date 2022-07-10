from Tests.TestBase import VulkanTesterBase


class VulkanSpotifyTest(VulkanTesterBase):
    def __init__(self) -> None:
        super().__init__()

    def test_spotifyTrack(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_TRACK_URL))

        if len(musics) > 0:
            return True
        else:
            return False

    def test_spotifyPlaylist(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_PLAYLIST_URL))

        if len(musics) > 0:
            return True
        else:
            return False

    def test_spotifyArtist(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_ARTIST_URL))

        if len(musics) > 0:
            return True
        else:
            return False

    def test_spotifyAlbum(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_ARTIST_URL))

        if len(musics) > 0:
            return True
        else:
            return False

    def test_spotifyWrongUrlOne(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_WRONG1_URL))

        print(musics)
        if len(musics) == 0:
            return True
        else:
            return False

    def test_spotifyWrongUrlTwo(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_WRONG2_URL))

        print(musics)
        if len(musics) == 0:
            return True
        else:
            return False
