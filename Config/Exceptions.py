from Config.Messages import Messages


class VulkanError(Exception):
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


class ImpossibleMove(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        message = Messages()
        if title == '':
            title = message.IMPOSSIBLE_MOVE
        super().__init__(message, title, *args)


class MusicUnavailable(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class YoutubeError(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class BadCommandUsage(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class DownloadingError(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class SpotifyError(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class DeezerError(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class UnknownError(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class InvalidInput(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class WrongLength(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class ErrorMoving(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class ErrorRemoving(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class InvalidIndex(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)


class NumberRequired(VulkanError):
    def __init__(self, message='', title='', *args: object) -> None:
        super().__init__(message, title, *args)
