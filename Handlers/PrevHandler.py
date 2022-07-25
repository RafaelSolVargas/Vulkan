from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Config.Exceptions import BadCommandUsage, ImpossibleMove
from Handlers.HandlerResponse import HandlerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class PrevHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        processManager = ProcessManager()
        processInfo = processManager.getPlayerInfo(self.guild, self.ctx)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playlist = processInfo.getPlaylist()
        if len(playlist.getHistory()) == 0:
            error = ImpossibleMove()
            embed = self.embeds.NOT_PREVIOUS_SONG()
            return HandlerResponse(self.ctx, embed, error)

        if not self.__user_connected():
            error = ImpossibleMove()
            embed = self.embeds.NO_CHANNEL()
            return HandlerResponse(self.ctx, embed, error)

        if playlist.isLoopingAll() or playlist.isLoopingOne():
            error = BadCommandUsage()
            embed = self.embeds.FAIL_DUE_TO_LOOP_ON()
            return HandlerResponse(self.ctx, embed, error)

        # If not started, start the player process
        process = processInfo.getProcess()
        if not process.is_alive():
            process.start()

        # Send a prev command, together with the user voice channel
        prevCommand = VCommands(VCommandsType.PREV, self.ctx.author.voice.channel.id)
        queue = processInfo.getQueue()
        queue.put(prevCommand)
        return HandlerResponse(self.ctx)

    def __user_connected(self) -> bool:
        if self.ctx.author.voice:
            return True
        else:
            return False
