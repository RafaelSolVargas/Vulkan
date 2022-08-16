from abc import ABC, abstractmethod


class AbstractView(ABC):
    @abstractmethod
    async def update(self) -> None:
        pass

    def set_message(self, message) -> None:
        pass

    @abstractmethod
    def stopView(self) -> None:
        pass
