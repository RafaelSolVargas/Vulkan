import asyncio
from typing import List
import unittest
from Music.Downloader import Downloader
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
        self.constants = TestsConstants()
        super().__init__(methodName)

    @myAsyncTest
    async def test_emptyString(self):
        musicsList = await self.downloader.extract_info('')

        self.assertEqual(musicsList, [], self.constants.EMPTY_STRING_ERROR_MSG)

    @myAsyncTest
    async def test_YoutubeMusicUrl(self) -> None:
        musicInfo = await self.downloader.extract_info(self.constants.YOUTUBE_MUSIC_URL)

        self.assertTrue(self.__infoExtractedSuccessfully(musicInfo))

    def test_musicTitle(self):
        playlist = Playlist()
        song = Song(self.constants.MUSIC_TITLE_STRING, playlist, '')
        playlist.add_song(song)

        self.downloader.finish_one_song(song)
        self.assertFalse(song.problematic)

    def __downloadSucceeded(self, downloadReturn: List[dict]) -> bool:
        # print(downloadReturn)
        return True

    def __infoExtractedSuccessfully(self, info: List[dict]) -> bool:
        if len(info) > 0:
            return True
        else:
            return False


if __name__ == 'main':
    unittest.main()
