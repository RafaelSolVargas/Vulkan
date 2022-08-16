from typing import List
from discord import Message
from discord.ui import View
from Config.Emojis import VEmojis
from Music.VulkanBot import VulkanBot
from UI.Views.AbstractView import AbstractView
from UI.Buttons.AbstractItem import AbstractItem

emojis = VEmojis()


class BasicView(View, AbstractView):
    """View that receives buttons to hold, in timeout disable buttons"""

    def __init__(self, bot: VulkanBot, buttons: List[AbstractItem], timeout: float = 6000):
        super().__init__(timeout=timeout)
        self.__bot = bot
        self.__message: Message = None
        self.__working = True

        for button in buttons:
            # Set the buttons to have a instance of the view that contains them
            button.set_view(self)
            self.add_item(button)

    def stopView(self):
        self.__working = False

    async def on_timeout(self) -> None:
        # Disable all itens and, if has the message, edit it
        try:
            if not self.__working:
                return

            self.disable_all_items()
            if self.__message is not None and isinstance(self.__message, Message):
                await self.__message.edit(f"{emojis.MUSIC} - The buttons in this message have been disabled due timeout", view=self)
        except Exception as e:
            print(f'[ERROR EDITING MESSAGE] -> {e}')

    def set_message(self, message: Message) -> None:
        self.__message = message

    async def update(self):
        try:
            if not self.__working:
                return

            if self.__message is not None:
                await self.__message.edit(view=self)
        except Exception as e:
            print(f'[ERROR UPDATING MESSAGE] -> {e}')
