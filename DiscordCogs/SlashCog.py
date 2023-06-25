from discord.ext.commands import slash_command, Cog
from discord import Option, ApplicationContext, OptionChoice
from Handlers.ClearHandler import ClearHandler
from Handlers.MoveHandler import MoveHandler
from Handlers.NowPlayingHandler import NowPlayingHandler
from Handlers.PlayHandler import PlayHandler
from Handlers.PrevHandler import PrevHandler
from Handlers.RemoveHandler import RemoveHandler
from Handlers.ResetHandler import ResetHandler
from Handlers.ShuffleHandler import ShuffleHandler
from Handlers.SkipHandler import SkipHandler
from Handlers.PauseHandler import PauseHandler
from Handlers.StopHandler import StopHandler
from Handlers.ResumeHandler import ResumeHandler
from Handlers.HistoryHandler import HistoryHandler
from Handlers.QueueHandler import QueueHandler
from Handlers.LoopHandler import LoopHandler
from Handlers.VolumeHandler import VolumeHandler
from Messages.MessagesCategory import MessagesCategory
from Messages.Responses.SlashEmbedResponse import SlashEmbedResponse
from Music.VulkanBot import VulkanBot
from Config.Embeds import VEmbeds
from Config.Helper import Helper
import traceback

helper = Helper()


class SlashCommands(Cog):
    """
    Class to listen to Music commands
    It'll listen for commands from discord, when triggered will create a specific Handler for the command
    Execute the handler and then create a specific View to be showed in Discord
    """

    def __init__(self, bot: VulkanBot) -> None:
        self.__bot: VulkanBot = bot
        self.__embeds = VEmbeds()

    @slash_command(name="play", description=helper.HELP_PLAY)
    async def play(self, ctx: ApplicationContext,
                   music: Option(str, "The music name or URL", required=True)) -> None:
        # Due to the utilization of multiprocessing module in this Project, we have multiple instances of the Bot, and by using this flag
        # we can control witch bot instance will listen to the commands that Discord send to our application
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = PlayHandler(ctx, self.__bot)

            response = await controller.run(music)
            if response is not None:
                cogResponser1 = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
                await cogResponser1.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name="queue", description=helper.HELP_QUEUE)
    async def queue(self, ctx: ApplicationContext,
                    page_number: Option(int, helper.SLASH_QUEUE_DESCRIPTION, min_value=1, default=1)) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = QueueHandler(ctx, self.__bot)

            # Change index 1 to 0
            page_number -= 1
            response = await controller.run(page_number)

            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.QUEUE)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name="skip", description=helper.HELP_SKIP)
    async def skip(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = SkipHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='stop', description=helper.HELP_STOP)
    async def stop(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = StopHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='pause', description=helper.HELP_PAUSE)
    async def pause(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = PauseHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='resume', description=helper.HELP_RESUME)
    async def resume(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = ResumeHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='previous', description=helper.HELP_PREV)
    async def previous(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = PrevHandler(ctx, self.__bot)

            response = await controller.run()
            if response is not None:
                cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
                await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='history', description=helper.HELP_HISTORY)
    async def history(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = HistoryHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.HISTORY)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='loop', description=helper.HELP_LOOP)
    async def loop(self, ctx: ApplicationContext,
                   loop_type: Option(str, choices=[
                       OptionChoice(name='off', value='off'),
                       OptionChoice(name='one', value='one'),
                       OptionChoice(name='all', value='all')
                   ])) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = LoopHandler(ctx, self.__bot)

            response = await controller.run(loop_type)
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.LOOP)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='clear', description=helper.HELP_CLEAR)
    async def clear(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = ClearHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='now_playing', description=helper.HELP_NP)
    async def now_playing(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = NowPlayingHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.NOW_PLAYING)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='shuffle_songs', description=helper.HELP_SHUFFLE)
    async def shuffle(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = ShuffleHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='move_song', description=helper.SLASH_MOVE_HELP)
    async def move(self, ctx: ApplicationContext,
                   from_pos: Option(int, "The position of song to move", min_value=1),
                   to_pos: Option(int, "The position to put the song, default 1", min_value=1, default=1)) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            if from_pos == 0:
                from_pos = 1

            controller = MoveHandler(ctx, self.__bot)

            response = await controller.run(from_pos, to_pos)
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.MANAGING_QUEUE)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='volume', description=helper.CHANGE_VOLUME_LONG)
    async def move(self, ctx: ApplicationContext,
                   volume: Option(float, "The new volume of the song", min_value=1, default= 100)) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()

            controller = VolumeHandler(ctx, self.__bot)

            response = await controller.run(f'{volume}')
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='remove', description=helper.HELP_REMOVE)
    async def remove(self, ctx: ApplicationContext,
                     position: Option(int, "The song position to remove", min_value=1)) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = RemoveHandler(ctx, self.__bot)

            response = await controller.run(position)
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.MANAGING_QUEUE)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')

    @slash_command(name='reset', description=helper.HELP_RESET)
    async def reset(self, ctx: ApplicationContext) -> None:
        if not self.__bot.listingSlash:
            return
        try:
            await ctx.defer()
            controller = ResetHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser = SlashEmbedResponse(response, ctx, MessagesCategory.PLAYER)
            await cogResponser.run()
        except Exception:
            print(f'[ERROR IN SLASH COMMAND] -> {traceback.format_exc()}')


def setup(bot):
    bot.add_cog(SlashCommands(bot))
