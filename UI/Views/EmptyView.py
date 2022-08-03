from typing import List
from discord import Button, Message
from discord.ui import View
from Config.Emojis import VEmojis
from Music.VulkanBot import VulkanBot

emojis = VEmojis()


class EmptyView(View):
    def __init__(self, bot: VulkanBot, buttons: List[Button], timeout: float = 6000):
        super().__init__(timeout=timeout)
        self.__bot = bot
        self.__message: Message = None

        for button in buttons:
            self.add_item(button)

    async def on_timeout(self) -> None:
        # Disable all itens and, if has the message, edit it
        try:
            self.disable_all_items()
            if self.__message is not None and isinstance(self.__message, Message):
                await self.__message.edit(view=self)
        except Exception as e:
            print(f'[ERROR EDITING MESSAGE] -> {e}')

    def set_message(self, message: Message) -> None:
        self.__message = message
