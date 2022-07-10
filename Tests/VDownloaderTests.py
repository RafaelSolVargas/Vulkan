from typing import List
from Tests.TestBase import VulkanTesterBase
from Music.Playlist import Playlist
from Music.Song import Song
from asyncio import Task


class VulkanDownloaderTest(VulkanTesterBase):
    def __init__(self) -> None:
        super().__init__()

    def test_emptyString(self) -> bool:
        musicsList = self._runner.run_coroutine(self._downloader.extract_info(''))

        if musicsList == []:
            return True
        else:
            return False

    def test_YoutubeMusicUrl(self) -> bool:
        musicsList = self._runner.run_coroutine(self._searcher.search(self._constants.YT_MUSIC_URL))

        if len(musicsList) > 0:
            print(musicsList[0])
            return True
        else:
            return False

    def test_YoutubeChannelPlaylist(self) -> None:
        # Search the link to determine names
        musicsList = self._runner.run_coroutine(
            self._searcher.search(self._constants.YT_CHANNEL_PLAYLIST_URL))

        if len(musicsList) == 0:
            return False

        # Create and store songs in list
        playlist = Playlist()
        songsList: List[Song] = []
        for info in musicsList:
            song = Song(identifier=info, playlist=playlist, requester='')
            playlist.add_song(song)
            songsList.append(song)

        # Create a list of coroutines without waiting for them
        tasks: List[Task] = []
        for song in songsList:
            tasks.append(self._downloader.download_song(song))

        # Send for runner to execute them concurrently
        self._runner.run_coroutines_list(tasks)

        for song in songsList:
            if song.problematic or song.title == None:
                return False

        return True

    def test_YoutubeMixPlaylist(self) -> None:
        # Search the link to determine names
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YT_MIX_URL))

        # Musics from Mix should download only the first music
        if len(musics) != 1:
            return False

        playlist = Playlist()
        song = Song(musics[0], playlist, '')
        playlist.add_song(song)

        self._runner.run_coroutine(self._downloader.download_song(song))

        if song.problematic:
            return False
        else:
            print(song.title)
            return True

    def test_musicTitle(self):
        playlist = Playlist()
        song = Song(self._constants.MUSIC_TITLE_STRING, playlist, '')
        playlist.add_song(song)

        self._runner.run_coroutine(self._downloader.download_song(song))

        if song.problematic:
            return False
        else:
            print(song.title)
            return True

    def test_YoutubePersonalPlaylist(self) -> None:
        musicsList = self._runner.run_coroutine(
            self._searcher.search(self._constants.YT_PERSONAL_PLAYLIST_URL))

        if len(musicsList) == 0:
            return False

        # Create and store songs in list
        playlist = Playlist()
        songsList: List[Song] = []
        for info in musicsList:
            song = Song(identifier=info, playlist=playlist, requester='')
            playlist.add_song(song)
            songsList.append(song)

        # Create a list of coroutines without waiting for them
        tasks: List[Task] = []
        for song in songsList:
            tasks.append(self._downloader.download_song(song))

        # Send for runner to execute them concurrently
        self._runner.run_coroutines_list(tasks)

        for song in songsList:
            if not song.problematic and song.title == None:
                return False

        return True
