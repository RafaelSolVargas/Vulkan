from msilib.schema import ControlEvent
from typing import Dict
from discord import Guild, Client, Embed
from discord.ext import commands
from discord.ext.commands import Context
from Config.Config import Configs
from Config.Helper import Helper
from Controllers.ClearController import ClearController
from Controllers.NowPlayingController import NowPlayingController
from Controllers.PlayerController import PlayersController
from Music.Player import Player
from Utils.Utils import is_connected
from Controllers.SkipController import SkipController
from Controllers.PauseController import PauseController
from Controllers.StopController import StopController
from Controllers.ResumeController import ResumeController
from Controllers.HistoryController import HistoryController
from Controllers.QueueController import QueueController
from Controllers.LoopController import LoopController
from Views.EmoteView import EmoteView
from Views.EmbedView import EmbedView


helper = Helper()


class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.__guilds: Dict[Guild, Player] = {}
        self.__bot: Client = bot
        self.__config = Configs()
        self.__controller = PlayersController(self.__bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.__controller = PlayersController(self.__bot)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        """Load a player when joining a guild"""
        self.__guilds[guild] = Player(self.__bot, guild)
        print(f'Player for guild {guild.name} created')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild) -> None:
        """Removes the player of the guild if banned"""
        if guild in self.__guilds.keys():
            self.__guilds.pop(guild, None)
            print(f'Player for guild {guild.name} destroyed')

    @commands.command(name="play", help=helper.HELP_PLAY, description=helper.HELP_PLAY_LONG, aliases=['p', 'tocar'])
    async def play(self, ctx: Context, *args) -> None:
        track = " ".join(args)
        requester = ctx.author.name

        player = self.__get_player(ctx)
        if player is None:
            await self.__send_embed(ctx, self.__config.ERROR_TITLE, self.__config.NO_GUILD, 'red')
            return

        if is_connected(ctx) is None:
            success = await player.connect(ctx)
            if success == False:
                await self.__send_embed(ctx, self.__config.IMPOSSIBLE_MOVE, self.__config.NO_CHANNEL, 'red')
                return

        await player.play(ctx, track, requester)

    @commands.command(name="queue", help=helper.HELP_QUEUE, description=helper.HELP_QUEUE_LONG, aliases=['q', 'fila'])
    async def queue(self, ctx: Context) -> None:
        player = self.__get_player(ctx)
        if player is None:
            return

        embed = await player.queue()
        await ctx.send(embed=embed)

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
        player = self.__get_player(ctx)
        if player is None:
            return

        if is_connected(ctx) is None:
            success = await player.connect(ctx)
            if success == False:
                await self.__send_embed(ctx, self.__config.IMPOSSIBLE_MOVE, self.__config.NO_CHANNEL, 'red')
                return

        await player.play_prev(ctx)

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
        view = EmbedView(response)
        await view.run()

    @commands.command(name='shuffle', help=helper.HELP_SHUFFLE, description=helper.HELP_SHUFFLE_LONG, aliases=['aleatorio'])
    async def shuffle(self, ctx: Context) -> None:
        player = self.__get_player(ctx)
        if player is None:
            return
        else:
            description = await player.shuffle()
            await self.__send_embed(ctx, self.__config.SONG_PLAYER, description, 'blue')

    @commands.command(name='move', help=helper.HELP_MOVE, description=helper.HELP_MOVE_LONG, aliases=['m', 'mover'])
    async def move(self, ctx: Context, pos1, pos2='1') -> None:
        player = self.__get_player(ctx)
        if player is None:
            return
        else:
            description = await player.move(pos1, pos2)
            await self.__send_embed(ctx, self.__config.SONG_PLAYER, description, 'blue')

    @commands.command(name='remove', help=helper.HELP_REMOVE, description=helper.HELP_REMOVE_LONG, aliases=['remover'])
    async def remove(self, ctx: Context, position) -> None:
        player = self.__get_player(ctx)
        if player is None:
            return
        else:
            description = await player.remove(position)
            await self.__send_embed(ctx, self.__config.SONG_PLAYER, description, 'blue')

    @commands.command(name='reset', help=helper.HELP_RESET, description=helper.HELP_RESET_LONG, aliases=['resetar'])
    async def reset(self, ctx: Context) -> None:
        player = self.__get_player(ctx)
        try:
            await player.force_stop()
            await player.stop()
            self.__guilds[ctx.guild] = Player(self.__bot, ctx.guild)
            player = self.__get_player(ctx)
            await player.force_stop()
        except Exception as e:
            print(f'DEVELOPER NOTE -> Reset Error: {e}')

        self.__guilds[ctx.guild] = Player(self.__bot, ctx.guild)
        player = self.__get_player(ctx)
        print(f'Player for guild {ctx.guild} created')

    async def __send_embed(self, ctx: Context, title='', description='', colour='grey') -> None:
        try:
            colour = self.__config.COLOURS[colour]
        except:
            colour = self.__config.COLOURS['grey']

        embedvc = Embed(
            title=title,
            description=description,
            colour=colour
        )
        await ctx.send(embed=embedvc)

    async def __clean_messages(self, ctx: Context) -> None:
        last_messages = await ctx.channel.history(limit=5).flatten()

        for message in last_messages:
            try:
                if message.author == self.__bot.user:
                    if len(message.embeds) > 0:
                        embed = message.embeds[0]
                        if len(embed.fields) > 0:
                            if embed.fields[0].name == 'Uploader:':
                                await message.delete()

            except:
                continue

    def __get_player(self, ctx: Context) -> Player:
        return self.__controller.get_player(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))
