from Music.Interfaces import ISong, IPlaylist


class Song(ISong):

    def __init__(self, identifier: str, playlist: IPlaylist, requester: str) -> None:
        self.__identifier = identifier
        self.__info = {'requester': requester}
        self.__problematic = False
        self.__playlist: IPlaylist = playlist

    def finish_down(self, info: dict) -> None:
        self.__usefull_keys = ['duration',
                               'title', 'webpage_url',
                               'channel', 'id', 'uploader',
                               'thumbnail', 'original_url']
        self.__required_keys = ['url']

        for key in self.__required_keys:
            if key in info:
                self.__info[key] = info[key]
            else:
                print(f'DEVELOPER NOTE -> {key} not found in info of music: {self.identifier}')
                self.destroy()

        for key in self.__usefull_keys:
            if key in info:
                self.__info[key] = info[key]
            else:
                print(f'DEVELOPER NOTE -> {key} not found in info of music: {self.identifier}')

    @property
    def source(self) -> str:
        if 'url' in self.__info.keys():
            return self.__info['url']
        else:
            return None

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
        else:
            return 0.0

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def problematic(self) -> bool:
        return self.__problematic

    def destroy(self) -> None:
        print(f'DEVELOPER NOTE -> Music self destroying {self.__identifier}')
        self.__problematic = True
        self.__playlist.destroy_song(self)

    @property
    def info(self):
        return self.__info
