from Tests.TestBase import VulkanTesterBase
from Config.Exceptions import YandexMusicError


class VulkanYandexMusicTest(VulkanTesterBase):
    def __init__(self) -> None:
        super().__init__()

    def test_yandexTrack(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YANDEX_MUSIC_TRACK_URL))
        
        if len(musics) > 0:
            return True
        else:
            return False
        
    def test_yandexPlaylist(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YANDEX_MUSIC_PLAYLIST_URL))
        
        if len(musics) > 0:
            return True
        else:
            return False
    
    def test_yandexArtist(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YANDEX_MUSIC_ARTIST_URL))
        
        if len(musics) > 0:
            return True
        else:
            return False
    
    def test_yandexAlbum(self) -> bool:
        musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YANDEX_MUSIC_ALBUM_URL))
        
        if len(musics) > 0:
            return True
        else:
            return False
    
    def test_yandexWrongUrlShouldThrowException(self) -> bool:
        try:
           musics = self._runner.run_coroutine(
            self._searcher.search(self._constants.YANDEX_MUSIC_WRONG1_URL))
        
        except YandexMusicError as e:
            print(f'Yandex Music Error -> {e.message}')
            return True
        except Exception as e:
            print(e)
            return False
    
    def test_yandexWrongUrlTwoShouldThrowException(self) -> bool:
        try:
            musics = self._runner.run_coroutine(
                self._searcher.search(self._constants.YANDEX_MUSIC_WRONG2_URL))
        
        except YandexMusicError as e:
            print(f'Yandex Music Error -> {e.message}')
            return True
        except Exception as e:
            print(e)
            return False
  