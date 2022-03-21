from vulkan.views.AbstractView import AbstractView
from vulkan.results import AbstractResult


class MessageView(AbstractView):
    def __init__(self, result: AbstractResult) -> None:
        super().__init__(result)

    def run(self) -> None:
        return super().run()
