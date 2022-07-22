from discord import Guild, Client
from discord.ext import commands
from discord.ext.commands import Context
from Config.Helper import Helper
from Controllers.ClearController import ClearController
from Controllers.MoveController import MoveController
from Controllers.NowPlayingController import NowPlayingController
from Controllers.PlayController import PlayController
from Controllers.PlayersController import PlayersController
from Controllers.PrevController import PrevController
from Controllers.RemoveController import RemoveController
from Controllers.ResetController import ResetController
from Controllers.ShuffleController import ShuffleController
from Utils.Cleaner import Cleaner
from Controllers.SkipController import SkipController
from Controllers.PauseController import PauseController
from Controllers.StopController import StopController
from Controllers.ResumeController import ResumeController
from Controllers.HistoryController import HistoryController
from Controllers.QueueController import QueueController
from Controllers.LoopController import LoopController
from Views.EmoteView import EmoteView
from Views.EmbedView import EmbedView
from Parallelism.ProcessManager import ProcessManager

helper = Helper()


class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.__bot: Client = bot
        self.__processManager = ProcessManager(bot)
        self.__cleaner = Cleaner(self.__bot)
        self.__controller = PlayersController(self.__bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.__controller = PlayersController(self.__bot)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        self.__controller.create_player(guild)

    @commands.command(name="play", help=helper.HELP_PLAY, description=helper.HELP_PLAY_LONG, aliases=['p', 'tocar'])
    async def play(self, ctx: Context, *args) -> None:
        controller = PlayController(ctx, self.__bot)

        response = await controller.run(args)
        if response is not None:
            view1 = EmbedView(response)
            view2 = EmoteView(response)
            await view1.run()
            await view2.run()

    @commands.command(name="queue", help=helper.HELP_QUEUE, description=helper.HELP_QUEUE_LONG, aliases=['q', 'fila'])
    async def queue(self, ctx: Context) -> None:
        controller = QueueController(ctx, self.__bot)

        response = await controller.run()
        view2 = EmbedView(response)
        await view2.run()

    @commands.command(name="skip", help=helper.HELP_SKIP, description=helper.HELP_SKIP_LONG, aliases=['s', 'pular'])
    async def skip(self, ctx: Context) -> None:
        controller = SkipController(ctx, self.__bot)

        response = await controller.run()
        if response.success:
            view = EmoteView(response)
        else:
            view = EmbedView(response)

        await view.run()

    @commands.command(name='stop', help=helper.HELP_STOP, description=helper.HELP_STOP_LONG, aliases=['parar'])
    async def stop(self, ctx: Context) -> None:
        controller = StopController(ctx, self.__bot)

        response = await controller.run()
        if response.success:
            view = EmoteView(response)
        else:
            view = EmbedView(response)

        await view.run()

    @commands.command(name='pause', help=helper.HELP_PAUSE, description=helper.HELP_PAUSE_LONG, aliases=['pausar'])
    async def pause(self, ctx: Context) -> None:
        controller = PauseController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmoteView(response)
        view2 = EmbedView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='resume', help=helper.HELP_RESUME, description=helper.HELP_RESUME_LONG, aliases=['soltar'])
    async def resume(self, ctx: Context) -> None:
        controller = ResumeController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmoteView(response)
        view2 = EmbedView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='prev', help=helper.HELP_PREV, description=helper.HELP_PREV_LONG, aliases=['anterior'])
    async def prev(self, ctx: Context) -> None:
        controller = PrevController(ctx, self.__bot)

        response = await controller.run()
        if response is not None:
            view1 = EmbedView(response)
            view2 = EmoteView(response)
            await view1.run()
            await view2.run()

    @commands.command(name='history', help=helper.HELP_HISTORY, description=helper.HELP_HISTORY_LONG, aliases=['historico'])
    async def history(self, ctx: Context) -> None:
        controller = HistoryController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='loop', help=helper.HELP_LOOP, description=helper.HELP_LOOP_LONG, aliases=['l', 'repeat'])
    async def loop(self, ctx: Context, args='') -> None:
        controller = LoopController(ctx, self.__bot)

        response = await controller.run(args)
        view1 = EmoteView(response)
        view2 = EmbedView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='clear', help=helper.HELP_CLEAR, description=helper.HELP_CLEAR_LONG, aliases=['c', 'limpar'])
    async def clear(self, ctx: Context) -> None:
        controller = ClearController(ctx, self.__bot)

        response = await controller.run()
        view = EmoteView(response)
        await view.run()

    @commands.command(name='np', help=helper.HELP_NP, description=helper.HELP_NP_LONG, aliases=['playing', 'now'])
    async def now_playing(self, ctx: Context) -> None:
        controller = NowPlayingController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='shuffle', help=helper.HELP_SHUFFLE, description=helper.HELP_SHUFFLE_LONG, aliases=['aleatorio'])
    async def shuffle(self, ctx: Context) -> None:
        controller = ShuffleController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='move', help=helper.HELP_MOVE, description=helper.HELP_MOVE_LONG, aliases=['m', 'mover'])
    async def move(self, ctx: Context, pos1, pos2='1') -> None:
        controller = MoveController(ctx, self.__bot)

        response = await controller.run(pos1, pos2)
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='remove', help=helper.HELP_REMOVE, description=helper.HELP_REMOVE_LONG, aliases=['remover'])
    async def remove(self, ctx: Context, position) -> None:
        controller = RemoveController(ctx, self.__bot)

        response = await controller.run(position)
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()

    @commands.command(name='reset', help=helper.HELP_RESET, description=helper.HELP_RESET_LONG, aliases=['resetar'])
    async def reset(self, ctx: Context) -> None:
        controller = ResetController(ctx, self.__bot)

        response = await controller.run()
        view1 = EmbedView(response)
        view2 = EmoteView(response)
        await view1.run()
        await view2.run()


def setup(bot):
    bot.add_cog(Music(bot))
