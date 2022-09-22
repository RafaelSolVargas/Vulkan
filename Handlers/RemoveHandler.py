from discord.ext.commands import Context
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import BadCommandUsage, VulkanError, ErrorRemoving, InvalidInput, NumberRequired
from Music.Playlist import Playlist
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessInfo import ProcessInfo
from typing import Union
from discord import Interaction


class RemoveHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, position: str) -> HandlerResponse:
        # Get the current process of the guild
        processManager = self.config.getProcessManager()
        processInfo: ProcessInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playlist = processInfo.getPlaylist()
        if playlist is None:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        error = self.__validateInput(position)
        if error:
            embed = self.embeds.ERROR_EMBED(error.message)
            return HandlerResponse(self.ctx, embed, error)

        position = self.__sanitizeInput(playlist, position)
        if not playlist.validate_position(position):
            error = InvalidInput()
            embed = self.embeds.PLAYLIST_RANGE_ERROR()
            return HandlerResponse(self.ctx, embed, error)

        try:
            song = playlist.remove_song(position)
            name = song.title if song.title else song.identifier

            embed = self.embeds.SONG_REMOVED(name)
            return HandlerResponse(self.ctx, embed)
        except:
            error = ErrorRemoving()
            embed = self.embeds.ERROR_REMOVING()
            return HandlerResponse(self.ctx, embed, error)

    def __validateInput(self, position: str) -> Union[VulkanError, None]:
        try:
            position = int(position)
        except:
            return NumberRequired(self.messages.ERROR_NUMBER)

    def __sanitizeInput(self, playlist: Playlist, position: str) -> int:
        position = int(position)

        if position == -1:
            position = len(playlist.getSongs())
        return position
