from Views.AbstractView import AbstractView
from Controllers.ControllerResponse import ControllerResponse


class EmbedView(AbstractView):
    def __init__(self, response: ControllerResponse) -> None:
        super().__init__(response)

    async def run(self) -> None:
        if self.response.embed:
            await self.context.send(embed=self.response.embed)
