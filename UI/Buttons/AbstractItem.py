from abc import ABC, abstractmethod
from discord.ui import Item, View


class AbstractItem(ABC, Item):
    @abstractmethod
    def set_view(self, view: View):
        pass

    @abstractmethod
    def get_view(self) -> View:
        pass
