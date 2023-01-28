from time import time


class Song:
    def __init__(self, identifier: str, playlist, requester: str) -> None:
        self.__identifier = identifier
        self.__info = {'requester': requester}
        self.__problematic = False
        self.__playlist = playlist
        self.__downloadTime: int = time()

    def finish_down(self, info: dict) -> None:
        if info is None or info == {}:
            self.destroy()
            return None

        self.__downloadTime = time()
        self.__useful_keys = ['duration',
                              'title', 'webpage_url',
                              'channel', 'id', 'uploader',
                              'thumbnail', 'original_url']
        self.__required_keys = ['url']

        for key in self.__required_keys:
            if key in info.keys():
                self.__info[key] = info[key]
            else:
                print(
                    f'DEVELOPER NOTE -> Required information [{key}] was not found in the music: {self.identifier}')
                self.destroy()
                return

        for key in self.__useful_keys:
            if key in info.keys():
                self.__info[key] = info[key]

        self.__cleanTitle()

    def __cleanTitle(self) -> None:
        self.__info['title'] = ''.join(char if char.isalnum() or char ==
                                       ' ' else ' ' for char in self.__info['title'])

    @property
    def downloadTime(self) -> int:
        return self.__downloadTime

    @property
    def source(self) -> str:
        if 'url' in self.__info.keys():
            return self.__info['url']
        else:
            return None

    @source.setter
    def source(self, value) -> None:
        self.__info['url'] = value

    @property
    def title(self) -> str:
        if 'title' in self.__info.keys():
            return self.__info['title']
        else:
            return None

    @property
    def duration(self) -> str:
        if 'duration' in self.__info.keys():
            return self.__info['duration']
        else:  # Default minimum duration
            return 5.0

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value) -> None:
        self.__identifier = value

    @property
    def problematic(self) -> bool:
        return self.__problematic

    def destroy(self) -> None:
        print(f'MUSIC ERROR -> Music self destroying {self.__identifier}')
        self.__problematic = True
        self.__playlist.destroy_song(self)

    @property
    def info(self):
        return self.__info
