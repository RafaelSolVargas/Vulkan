from Config.Emojis import VEmojis
from Messages.Responses.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory


class EmoteCommandResponse(AbstractCommandResponse):

    def __init__(self, response: HandlerResponse, category: MessagesCategory) -> None:
        super().__init__(response, category)
        self.__emojis = VEmojis()

    async def run(self, deleteLast: bool = True) -> None:
        if self.response.success:
            await self.message.add_reaction(self.__emojis.SUCCESS)
        else:
            await self.message.add_reaction(self.__emojis.ERROR)
