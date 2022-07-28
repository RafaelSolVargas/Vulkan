from discord.ui import View
from Config.Emojis import VEmojis
from UI.Buttons.PauseButton import PauseButton
from UI.Buttons.BackButton import BackButton
from UI.Buttons.SkipButton import SkipButton
from UI.Buttons.StopButton import StopButton
from UI.Buttons.SongsButton import SongsButton
from UI.Buttons.PlayButton import PlayButton
from UI.Buttons.LoopAllButton import LoopAllButton
from UI.Buttons.LoopOneButton import LoopOneButton
from UI.Buttons.LoopOffButton import LoopOffButton
from Music.VulkanBot import VulkanBot

emojis = VEmojis()


class PlayerView(View):
    def __init__(self, bot: VulkanBot, timeout: float = 180):
        super().__init__(timeout=timeout)
        self.__bot = bot
        self.add_item(BackButton(self.__bot))
        self.add_item(PauseButton(self.__bot))
        self.add_item(PlayButton(self.__bot))
        self.add_item(StopButton(self.__bot))
        self.add_item(SkipButton(self.__bot))
        self.add_item(SongsButton(self.__bot))
        self.add_item(LoopOneButton(self.__bot))
        self.add_item(LoopOffButton(self.__bot))
        self.add_item(LoopAllButton(self.__bot))
