import asyncio
from typing import List
import unittest
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Music.Playlist import Playlist
from Music.Song import Song
from Tests.TestsHelper import TestsConstants


def myAsyncTest(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class TestDownloader(unittest.IsolatedAsyncioTestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.downloader = Downloader()
        self.searcher = Searcher()
        self.constants = TestsConstants()
        super().__init__(methodName)

    @myAsyncTest
    async def test_emptyString(self):
        musicsList = await self.downloader.extract_info('')

        self.assertEqual(musicsList, [], self.constants.EMPTY_STRING_ERROR_MSG)

    @myAsyncTest
    async def test_YoutubeMusicUrl(self) -> None:
        musics = await self.searcher.search(self.constants.YT_MUSIC_URL)

        self.assertTrue(len(musics) > 0)

    @myAsyncTest
    async def test_YoutubePersonalPlaylist(self) -> None:
        musics = await self.searcher.search(self.constants.YT_PERSONAL_PLAYLIST_URL)

        self.assertTrue(len(musics) > 0)

    @myAsyncTest
    async def test_YoutubeChannelPlaylist(self) -> None:
        # Search the link to determine names
        musicsInfo = await self.searcher.search(self.constants.YT_CHANNEL_PLAYLIST_URL)

        self.assertTrue(len(musicsInfo) > 0)

        # Create and store songs in list
        playlist = Playlist()
        songsList = []
        for info in musicsInfo:
            song = Song(identifier=info, playlist=playlist, requester='')
            playlist.add_song(song)
            songsList.append(song)

        # We need to trigger and wait multiple tasks, so we create multiple tasks with asyncio
        # and then we await for each one of them. We use this because download_song is a Coroutine
        tasks: List[asyncio.Task] = []
        for song in songsList:
            task = asyncio.create_task(self.downloader.download_song(song))
            tasks.append(task)

        # Await for each task to finish
        for task in tasks:
            await task

        self.assertTrue(self.__verifySuccessfullyPreload(songsList))

    @myAsyncTest
    async def test_YoutubeMixPlaylist(self) -> None:
        music = await self.searcher.search(self.constants.YT_MIX_URL)

        # Musics from Mix should download only the first music
        self.assertTrue(len(music) == 1)

    @myAsyncTest
    async def test_musicTitle(self):
        playlist = Playlist()
        song = Song(self.constants.MUSIC_TITLE_STRING, playlist, '')
        playlist.add_song(song)

        task = asyncio.create_task(self.downloader.download_song(song))
        await task

        self.assertFalse(song.problematic)

    def __verifySuccessfullyPreload(self, songs: List[Song]) -> bool:
        for song in songs:
            if song.title == None:
                print('Song failed to download')
                return False

        return True


if __name__ == 'main':
    unittest.main()
