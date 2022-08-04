from Messages.Responses.AbstractCogResponse import AbstractCommandResponse
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory


class EmbedCommandResponse(AbstractCommandResponse):
    def __init__(self, response: HandlerResponse, category: MessagesCategory) -> None:
        super().__init__(response, category)

    async def run(self, deleteLast: bool = True) -> None:
        if self.response.embed and self.response.view:
            message = await self.context.send(embed=self.response.embed, view=self.response.view)
        elif self.response.embed:
            message = await self.context.send(embed=self.response.embed)

            # Only delete the previous message if this is not error and not forbidden by method caller
            if deleteLast and self.response.success:
                await self.manager.addMessageAndClearPrevious(self.context.guild.id, self.category, message)
            else:
                self.manager.addMessage(self.context.guild.id, self.category, message)
