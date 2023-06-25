from discord.ext.commands import Context, command, Cog
from Config.Exceptions import InvalidInput
from Config.Helper import Helper
from Handlers.ClearHandler import ClearHandler
from Handlers.HandlerResponse import HandlerResponse
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
from Messages.Responses.EmoteCogResponse import EmoteCommandResponse
from Messages.Responses.EmbedCogResponse import EmbedCommandResponse
from Music.VulkanBot import VulkanBot
from Config.Configs import VConfigs
from Config.Embeds import VEmbeds
from Parallelism.ProcessPlayerManager import ProcessPlayerManager
from Parallelism.ThreadPlayerManager import ThreadPlayerManager

helper = Helper()


class MusicCog(Cog):
    """
    Class to listen to Music commands
    It'll listen for commands from discord, when triggered will create a specific Handler for the command
    Execute the handler and then create a specific View to be showed in Discord
    """

    def __init__(self, bot: VulkanBot) -> None:
        self.__bot: VulkanBot = bot
        self.__embeds = VEmbeds()
        configs = VConfigs()
        if configs.SONG_PLAYBACK_IN_SEPARATE_PROCESS:
            configs.setPlayersManager(ProcessPlayerManager(bot))
        else:
            configs.setPlayersManager(ThreadPlayerManager(bot))

    @command(name="play", help=helper.HELP_PLAY, description=helper.HELP_PLAY_LONG, aliases=['p', 'tocar'])
    async def play(self, ctx: Context, *args) -> None:
        try:
            controller = PlayHandler(ctx, self.__bot)

            if len(args) > 1:
                track = " ".join(args)
            else:
                track = args[0]

            response = await controller.run(track)
            if response is not None:
                cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponser1.run()
                await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="volume", help=helper.CHANGE_VOLUME, description=helper.CHANGE_VOLUME_LONG, aliases=['v'])
    async def volume(self, ctx: Context, *args) -> None:
        try:
            controller = VolumeHandler(ctx, self.__bot)

            if len(args) > 1:
                track = " ".join(args)
            else:
                track = args[0]

            response = await controller.run(track)
            if response is not None:
                cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponser1.run()
                await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="queue", help=helper.HELP_QUEUE, description=helper.HELP_QUEUE_LONG, aliases=['q', 'fila', 'musicas'])
    async def queue(self, ctx: Context, *args) -> None:
        try:
            pageNumber = " ".join(args)

            controller = QueueHandler(ctx, self.__bot)

            if pageNumber == "":
                response = await controller.run()
            else:
                pageNumber = int(pageNumber)
                pageNumber -= 1  # Change index 1 to 0
                response = await controller.run(pageNumber)

            cogResponser = EmbedCommandResponse(response, MessagesCategory.QUEUE)
            await cogResponser.run()
        except ValueError as e:
            # Draft a Handler Response to pass to cogResponser
            error = InvalidInput()
            embed = self.__embeds.INVALID_ARGUMENTS()
            response = HandlerResponse(ctx, embed, error)

            cogResponser = EmbedCommandResponse(response, MessagesCategory.QUEUE)
            await cogResponser.run(deleteLast=False)
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name="skip", help=helper.HELP_SKIP, description=helper.HELP_SKIP_LONG, aliases=['s', 'pular', 'next'])
    async def skip(self, ctx: Context) -> None:
        try:
            controller = SkipHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='stop', help=helper.HELP_STOP, description=helper.HELP_STOP_LONG, aliases=['parar'])
    async def stop(self, ctx: Context) -> None:
        try:
            controller = StopHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='pause', help=helper.HELP_PAUSE, description=helper.HELP_PAUSE_LONG, aliases=['pausar', 'pare'])
    async def pause(self, ctx: Context) -> None:
        try:
            controller = PauseHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='resume', help=helper.HELP_RESUME, description=helper.HELP_RESUME_LONG, aliases=['soltar', 'despausar'])
    async def resume(self, ctx: Context) -> None:
        try:
            controller = ResumeHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='prev', help=helper.HELP_PREV, description=helper.HELP_PREV_LONG, aliases=['anterior', 'return', 'previous', 'back'])
    async def prev(self, ctx: Context) -> None:
        try:
            controller = PrevHandler(ctx, self.__bot)

            response = await controller.run()
            if response is not None:
                cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
                cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
                await cogResponser1.run()
                await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='history', help=helper.HELP_HISTORY, description=helper.HELP_HISTORY_LONG, aliases=['historico', 'anteriores', 'hist'])
    async def history(self, ctx: Context) -> None:
        try:
            controller = HistoryHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.HISTORY)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.HISTORY)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='loop', help=helper.HELP_LOOP, description=helper.HELP_LOOP_LONG, aliases=['l', 'repeat'])
    async def loop(self, ctx: Context, args='') -> None:
        try:
            controller = LoopHandler(ctx, self.__bot)

            response = await controller.run(args)
            cogResponser1 = EmoteCommandResponse(response, MessagesCategory.LOOP)
            cogResponser2 = EmbedCommandResponse(response, MessagesCategory.LOOP)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='clear', help=helper.HELP_CLEAR, description=helper.HELP_CLEAR_LONG, aliases=['c', 'limpar'])
    async def clear(self, ctx: Context) -> None:
        try:
            controller = ClearHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='np', help=helper.HELP_NP, description=helper.HELP_NP_LONG, aliases=['playing', 'now', 'this'])
    async def now_playing(self, ctx: Context) -> None:
        try:
            controller = NowPlayingHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.NOW_PLAYING)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.NOW_PLAYING)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='shuffle', help=helper.HELP_SHUFFLE, description=helper.HELP_SHUFFLE_LONG, aliases=['aleatorio', 'misturar'])
    async def shuffle(self, ctx: Context) -> None:
        try:
            controller = ShuffleHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='move', help=helper.HELP_MOVE, description=helper.HELP_MOVE_LONG, aliases=['m', 'mover'])
    async def move(self, ctx: Context, pos1, pos2='1') -> None:
        try:
            controller = MoveHandler(ctx, self.__bot)

            response = await controller.run(pos1, pos2)
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='remove', help=helper.HELP_REMOVE, description=helper.HELP_REMOVE_LONG, aliases=['remover'])
    async def remove(self, ctx: Context, position) -> None:
        try:
            controller = RemoveHandler(ctx, self.__bot)

            response = await controller.run(position)
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.MANAGING_QUEUE)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')

    @command(name='reset', help=helper.HELP_RESET, description=helper.HELP_RESET_LONG, aliases=['resetar'])
    async def reset(self, ctx: Context) -> None:
        try:
            controller = ResetHandler(ctx, self.__bot)

            response = await controller.run()
            cogResponser1 = EmbedCommandResponse(response, MessagesCategory.PLAYER)
            cogResponser2 = EmoteCommandResponse(response, MessagesCategory.PLAYER)
            await cogResponser1.run()
            await cogResponser2.run()
        except Exception as e:
            print(f'[ERROR IN COG] -> {e}')


def setup(bot):
    bot.add_cog(MusicCog(bot))
