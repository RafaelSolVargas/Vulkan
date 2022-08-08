from typing import Union
from Config.Exceptions import BadCommandUsage, InvalidInput, NumberRequired, UnknownError, VulkanError
from Handlers.AbstractHandler import AbstractHandler
from discord.ext.commands import Context
from discord import Interaction
from Handlers.HandlerResponse import HandlerResponse
from Music.Playlist import Playlist
from Music.VulkanBot import VulkanBot
from Parallelism.Commands import VCommands, VCommandsType


class JumpMusicHandler(AbstractHandler):
    """Move a music from a specific position and play it directly"""

    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, musicPos: str) -> HandlerResponse:
        processManager = self.config.getProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        processLock = processInfo.getLock()
        acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        if acquired:
            # Try to convert input to int
            error = self.__validateInput(musicPos)
            if error:
                embed = self.embeds.ERROR_EMBED(error.message)
                processLock.release()
                return HandlerResponse(self.ctx, embed, error)

            # Sanitize the input
            playlist: Playlist = processInfo.getPlaylist()
            musicPos = self.__sanitizeInput(playlist, musicPos)

            # Validate the position
            if not playlist.validate_position(musicPos):
                error = InvalidInput()
                embed = self.embeds.PLAYLIST_RANGE_ERROR()
                processLock.release()
                return HandlerResponse(self.ctx, embed, error)
            try:
                # Move the selected song
                playlist.move_songs(musicPos, 1)

                # Send a command to the player to skip the music
                command = VCommands(VCommandsType.SKIP, None)
                queue = processInfo.getQueueToPlayer()
                queue.put(command)

                processLock.release()
                return HandlerResponse(self.ctx)
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

    def __validateInput(self, position: str) -> Union[VulkanError, None]:
        try:
            position = int(position)
        except:
            return NumberRequired(self.messages.ERROR_NUMBER)

    def __sanitizeInput(self, playlist: Playlist, position: int) -> int:
        position = int(position)

        if position == -1:
            position = len(playlist.getSongs())

        return position
