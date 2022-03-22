from Vulkan.Views.AbstractView import AbstractView
from Vulkan.Controllers.ControllerResponse import ControllerResponse


class EmoteView(AbstractView):

    def __init__(self, response: ControllerResponse) -> None:
        super().__init__(response)

    async def run(self) -> None:
        if self.response.success:
            await self.message.add_reaction('✅')
        else:
            await self.message.add_reaction('❌')
