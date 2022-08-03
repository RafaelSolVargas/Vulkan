from UI.Responses.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse


class EmbedCommandResponse(AbstractCommandResponse):
    def __init__(self, response: HandlerResponse) -> None:
        super().__init__(response)

    async def run(self) -> None:
        if self.response.embed:
            await self.context.send(embed=self.response.embed, view=self.response.view)
