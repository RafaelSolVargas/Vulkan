from Config.Exceptions import BadCommandUsage, NumberRequired, VulkanError
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Parallelism.Commands import VCommands, VCommandsType
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from discord.ext.commands import Context
from Music.VulkanBot import VulkanBot
from discord import Interaction
from typing import Union


class VolumeHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, args: str) -> HandlerResponse:
        if args is None or args.strip() == '':
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        error = self.__validateInput(args)
        if error:
            embed = self.embeds.ERROR_EMBED(error.message)
            return HandlerResponse(self.ctx, embed, error)

        playersManager: AbstractPlayersManager = self.config.getPlayersManager()
        if not playersManager.verifyIfPlayerExists(self.guild):
            embed = self.embeds.NOT_PLAYING()
            error = BadCommandUsage()
            return HandlerResponse(self.ctx, embed, error)

        playerLock = playersManager.getPlayerLock(self.guild)
        acquired = playerLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        volume = self.__convert_input_to_volume(args)        
        if acquired:
            volumeCommand = VCommands(VCommandsType.VOLUME, volume)
            await playersManager.sendCommandToPlayer(volumeCommand, self.guild, self.ctx)
            
            playerLock.release()
            
            embed = self.embeds.VOLUME_CHANGED(volume)
            return HandlerResponse(self.ctx, embed)
        else:
            playersManager.resetPlayer(self.guild, self.ctx)
            
            embed = self.embeds.PLAYER_RESTARTED()
            return HandlerResponse(self.ctx, embed)

    def __convert_input_to_volume(self, input_volume: str) -> float:
        volume = float(input_volume)
        if volume < 0:
            volume = 0
        if volume > 100:
            volume = 100
        
        return volume

    def __validateInput(self, volume: str) -> Union[VulkanError, None]:
        try:
            _ = float(volume)
        except:
            return NumberRequired(self.messages.ERROR_VOLUME_NUMBER)