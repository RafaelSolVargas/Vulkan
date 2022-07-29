from typing import Union
from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Config.Exceptions import BadCommandUsage, VulkanError, InvalidInput, NumberRequired, UnknownError
from Music.Playlist import Playlist
from typing import Union
from discord import Interaction


class MoveHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, pos1: str, pos2: str) -> HandlerResponse:
        processManager = self.config.getProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        processLock = processInfo.getLock()
        acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        if acquired:
            error = self.__validateInput(pos1, pos2)
            if error:
                embed = self.embeds.ERROR_EMBED(error.message)
                processLock.release()
                return HandlerResponse(self.ctx, embed, error)

            playlist = processInfo.getPlaylist()
            pos1, pos2 = self.__sanitizeInput(playlist, pos1, pos2)

            if not playlist.validate_position(pos1) or not playlist.validate_position(pos2):
                error = InvalidInput()
                embed = self.embeds.PLAYLIST_RANGE_ERROR()
                processLock.release()
                return HandlerResponse(self.ctx, embed, error)
            try:
                song = playlist.move_songs(pos1, pos2)

                song_name = song.title if song.title else song.identifier
                embed = self.embeds.SONG_MOVED(song_name, pos1, pos2)
                processLock.release()
                return HandlerResponse(self.ctx, embed)
            except:
                # Release the acquired Lock
                processLock.release()
                embed = self.embeds.ERROR_MOVING()
                error = UnknownError()
                return HandlerResponse(self.ctx, embed, error)
        else:
            processManager.resetProcess(self.guild, self.ctx)
            embed = self.embeds.PLAYER_RESTARTED()
            return HandlerResponse(self.ctx, embed)

    def __validateInput(self, pos1: str, pos2: str) -> Union[VulkanError, None]:
        try:
            pos1 = int(pos1)
            pos2 = int(pos2)
        except:
            return NumberRequired(self.messages.ERROR_NUMBER)

    def __sanitizeInput(self, playlist: Playlist, pos1: int, pos2: int) -> tuple:
        pos1 = int(pos1)
        pos2 = int(pos2)

        if pos1 == -1:
            pos1 = len(playlist.getSongs())
        if pos2 == -1:
            pos2 = len(playlist.getSongs())

        return pos1, pos2
