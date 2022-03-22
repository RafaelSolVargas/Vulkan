from Config.Config import Configs


class Error(Exception):
    def __init__(self, message='', title='', *args: object) -> None:
        self.__message = message
        self.__title = title
        super().__init__(*args)

    @property
    def message(self) -> str:
        return self.__message

    @property
    def title(self) -> str:
        return self.__title


class ImpossibleMove(Error):
    def __init__(self, message='', title='', *args: object) -> None:
        config = Configs()
        if title == '':
            title = config.IMPOSSIBLE_MOVE
        super().__init__(message, title, *args)


class MusicUnavailable(Error):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class BadCommandUsage(Error):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class UnknownError(Error):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)
