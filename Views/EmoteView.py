from Views.AbstractView import AbstractView
from Handlers.HandlerResponse import HandlerResponse


class EmoteView(AbstractView):

    def __init__(self, response: HandlerResponse) -> None:
        super().__init__(response)

    async def run(self) -> None:
        if self.response.success:
            await self.message.add_reaction('✅')
        else:
            await self.message.add_reaction('❌')
