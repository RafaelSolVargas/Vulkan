from Config.Emojis import VEmojis
from Views.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse


class EmoteCommandResponse(AbstractCommandResponse):

    def __init__(self, response: HandlerResponse) -> None:
        super().__init__(response)
        self.__emojis = VEmojis()

    async def run(self) -> None:
        if self.response.success:
            await self.message.add_reaction(self.__emojis.SUCCESS)
        else:
            await self.message.add_reaction(self.__emojis.ERROR)
