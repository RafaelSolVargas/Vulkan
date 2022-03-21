from abc import ABC, abstractmethod


class Error(Exception, ABC):
    @abstractmethod
    def message():
        pass

    @abstractmethod
    def title():
        pass


class MusicUnavailable(Error):
    def __init__(self, message: str) -> None:
        self.__message = message
        super().__init__(message)

    def message():
        pass

    def title():
        pass

    def __str__(self) -> str:
        return self.__message
