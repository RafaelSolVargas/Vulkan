from abc import ABC, abstractproperty, abstractmethod


class IPlaylist(ABC):
    """Class to manage and control the songs to play and played"""


    @abstractproperty
    def looping_one(self):
        pass

    @abstractproperty
    def looping_all(self):
        pass

    @abstractproperty
    def songs_to_preload(self) -> list:
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def next_song(self):
        pass

    @abstractmethod
    def prev_song(self):
        pass

    @abstractmethod
    def add_song(self, identifier: str) -> None:
        pass

    @abstractmethod
    def shuffle(self) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def loop_one(self) -> str:
        pass

    @abstractmethod
    def loop_all(self) -> str:
        pass

    @abstractmethod
    def loop_off(self) -> str:
        pass

    @abstractmethod
    def destroy_song(self, song_destroy) -> None:
        pass


class ISong(ABC):
    """Store the usefull information about a Song"""

    @abstractmethod
    def finish_down(self, info: dict) -> None:
        pass

    @abstractmethod
    def source(self) -> str:
        pass

    @abstractmethod
    def title(self) -> str:
       pass

    @abstractmethod
    def duration(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:        
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass
        
