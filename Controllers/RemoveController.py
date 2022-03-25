from typing import Union
from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Exceptions.Exceptions import BadCommandUsage, Error, ErrorRemoving, InvalidInput, NumberRequired, UnknownError


class RemoveController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self, position: str) -> ControllerResponse:
        if not self.player.playlist:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return ControllerResponse(self.ctx, embed, error)

        error = self.__validate_input(position)
        if error:
            embed = self.embeds.ERROR_EMBED(error.message)
            return ControllerResponse(self.ctx, embed, error)

        position = self.__sanitize_input(position)
        if not self.player.playlist.validate_position(position):
            error = InvalidInput()
            embed = self.embeds.PLAYLIST_RANGE_ERROR()
            return ControllerResponse(self.ctx, embed, error)

        try:
            song = self.player.playlist.remove_song(position)
            name = song.title if song.title else song.identifier

            embed = self.embeds.SONG_REMOVED(name)
            return ControllerResponse(self.ctx, embed)
        except:
            error = ErrorRemoving()
            embed = self.embeds.ERROR_REMOVING()
            return ControllerResponse(self.ctx, embed, error)

    def __validate_input(self, position: str) -> Union[Error, None]:
        try:
            position = int(position)
        except:
            return NumberRequired(self.config.ERROR_NUMBER)

    def __sanitize_input(self, position: str) -> int:
        position = int(position)

        if position == -1:
            position = len(self.player.playlist)
        return position
