from typing import Union
from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Exceptions.Exceptions import BadCommandUsage, Error, InvalidInput, NumberRequired, UnknownError, WrongLength
from Music.Downloader import Downloader


class MoveController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__down = Downloader()

    async def run(self, pos1: str, pos2: str) -> ControllerResponse:
        if not self.player.playing:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return ControllerResponse(self.ctx, embed, error)

        error = self.__validate_input(pos1, pos2)
        if error:
            embed = self.embeds.ERROR_EMBED(error.message)
            return ControllerResponse(self.ctx, embed, error)

        pos1, pos2 = self.__sanitize_input(pos1, pos2)
        playlist = self.player.playlist

        if not playlist.validate_position(pos1) or not playlist.validate_position(pos2):
            error = InvalidInput()
            embed = self.embeds.PLAYLIST_RANGE_ERROR()
            return ControllerResponse(self.ctx, embed, error)
        try:
            song = self.player.playlist.move_songs(pos1, pos2)

            songs = self.player.playlist.songs_to_preload
            await self.__down.preload(songs)

            song_name = song.title if song.title else song.identifier
            embed = self.embeds.SONG_MOVED(song_name, pos1, pos2)
            return ControllerResponse(self.ctx, embed)
        except:
            embed = self.embeds.ERROR_MOVING()
            error = UnknownError()
            return ControllerResponse(self.ctx, embed, error)

    def __validate_input(self, pos1: str, pos2: str) -> Union[Error, None]:
        try:
            pos1 = int(pos1)
            pos2 = int(pos2)
        except:
            return NumberRequired(self.messages.ERROR_NUMBER)

    def __sanitize_input(self, pos1: int, pos2: int) -> tuple:
        pos1 = int(pos1)
        pos2 = int(pos2)

        if pos1 == -1:
            pos1 = len(self.player.playlist)
        if pos2 == -1:
            pos2 = len(self.player.playlist)

        return pos1, pos2
