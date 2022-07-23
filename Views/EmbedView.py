from Views.AbstractView import AbstractView
from Handlers.HandlerResponse import HandlerResponse


class EmbedView(AbstractView):
    def __init__(self, response: HandlerResponse) -> None:
        super().__init__(response)

    async def run(self) -> None:
        if self.response.embed:
            await self.context.send(embed=self.response.embed)
