from discord import Embed
from Config.Config import Configs
from Config.Colors import Colors
from datetime import timedelta


class Embeds:
    def __init__(self) -> None:
        self.__config = Configs()
        self.__colors = Colors()

    def ONE_SONG_LOOPING(self, info: dict) -> Embed:
        title = self.__config.ONE_SONG_LOOPING
        return self.SONG_INFO(info, title)

    def EMPTY_QUEUE(self) -> Embed:
        title = self.__config.SONG_PLAYER
        text = self.__config.EMPTY_QUEUE
        embed = Embed(
            title=title,
            description=text,
            colour=self.__colors.BLUE
        )
        return embed

    def INVALID_INPUT(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.INVALID_INPUT,
            colours=self.__colors.BLUE)
        return embed

    def UNAVAILABLE_VIDEO(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.VIDEO_UNAVAILABLE,
            colours=self.__colors.BLUE)
        return embed

    def DOWNLOADING_ERROR(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.DOWNLOADING_ERROR,
            colours=self.__colors.BLUE)
        return embed

    def SONG_ADDED(self, title: str) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONG_ADDED.format(title),
            colours=self.__colors.BLUE)
        return embed

    def SONGS_ADDED(self, quant: int) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONGS_ADDED.format(quant),
            colour=self.__colors.BLUE)
        return embed

    def SONG_INFO(self, info: dict, title: str, position='Playing Now') -> Embed:
        embedvc = Embed(
            title=title,
            description=f"[{info['title']}]({info['original_url']})",
            color=self.__colors.BLUE
        )

        embedvc.add_field(name=self.__config.SONGINFO_UPLOADER,
                          value=info['uploader'],
                          inline=False)

        embedvc.add_field(name=self.__config.SONGINFO_REQUESTER,
                          value=info['requester'],
                          inline=True)

        if 'thumbnail' in info.keys():
            embedvc.set_thumbnail(url=info['thumbnail'])

        if 'duration' in info.keys():
            duration = str(timedelta(seconds=info['duration']))
            embedvc.add_field(name=self.__config.SONGINFO_DURATION,
                              value=f"{duration}",
                              inline=True)
        else:
            embedvc.add_field(name=self.__config.SONGINFO_DURATION,
                              value=self.__config.SONGINFO_UNKNOWN_DURATION,
                              inline=True)

        embedvc.add_field(name=self.__config.SONGINFO_POSITION,
                          value=position,
                          inline=True)

        return embedvc

    def SONG_MOVED(self, song_name: str, pos1: int, pos2: int) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONG_MOVED_SUCCESSFULLY.format(song_name, pos1, pos2),
            colour=self.__colors.BLUE
        )
        return embed

    def ERROR_MOVING(self) -> Embed:
        embed = Embed(
            title=self.__config.UNKNOWN_ERROR,
            description=self.__config.ERROR_MOVING,
            colour=self.__colors.BLACK
        )
        return embed

    def ERROR_EMBED(self, description: str) -> Embed:
        embed = Embed(
            description=description,
            colour=self.__colors.BLACK
        )
        return embed

    def WRONG_LENGTH_INPUT(self) -> Embed:
        embed = Embed(
            title=self.__config.BAD_COMMAND_TITLE,
            description=self.__config.LENGTH_ERROR,
            colour=self.__colors.BLACK
        )
        return embed

    def BAD_LOOP_USE(self) -> Embed:
        embed = Embed(
            title=self.__config.BAD_COMMAND_TITLE,
            description=self.__config.BAD_USE_OF_LOOP,
            colour=self.__colors.BLACK
        )
        return embed

    def COMMAND_ERROR(self):
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.ERROR_MISSING_ARGUMENTS,
            colour=self.__colors.BLACK
        )
        return embed

    def COMMAND_NOT_FOUND(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.COMMAND_NOT_FOUND,
            colour=self.__colors.BLACK
        )
        return embed

    def MY_ERROR_BAD_COMMAND(self) -> Embed:
        embed = Embed(
            title=self.__config.BAD_COMMAND_TITLE,
            description=self.__config.BAD_COMMAND,
            colour=self.__colors.BLACK
        )
        return embed

    def UNKNOWN_ERROR(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.UNKNOWN_ERROR,
            colour=self.__colors.RED
        )
        return embed

    def FAIL_DUE_TO_LOOP_ON(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.LOOP_ON,
            colour=self.__colors.BLUE
        )
        return embed

    def ERROR_SHUFFLING(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.ERROR_SHUFFLING,
            colour=self.__colors.BLACK
        )
        return embed

    def SONGS_SHUFFLED(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONGS_SHUFFLED,
            colour=self.__colors.BLUE
        )
        return embed

    def LOOP_ONE_ACTIVATED(self) -> Embed:
        embed = Embed(
            title=self.__config.LOOP_ONE_ACTIVATE,
            colour=self.__colors.BLUE
        )
        return embed

    def LOOP_ALL_ACTIVATED(self) -> Embed:
        embed = Embed(
            title=self.__config.LOOP_ALL_ACTIVATE,
            colour=self.__colors.BLUE
        )
        return embed

    def NO_CHANNEL(self) -> Embed:
        embed = Embed(
            title=self.__config.IMPOSSIBLE_MOVE,
            description=self.__config.NO_CHANNEL,
            colour=self.__colors.BLACK
        )
        return embed

    def ERROR_DUE_LOOP_ONE_ON(self) -> Embed:
        embed = Embed(
            title=self.__config.BAD_COMMAND_TITLE,
            description=self.__config.ERROR_DUE_LOOP_ONE_ON,
            colour=self.__colors.BLACK
        )
        return embed

    def LOOP_DISABLE(self) -> Embed:
        embed = Embed(
            title=self.__config.LOOP_DISABLE,
            colour=self.__colors.BLUE
        )
        return embed

    def NOT_PREVIOUS_SONG(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.NOT_PREVIOUS,
            colour=self.__colors.BLUE
        )
        return embed

    def HISTORY(self, description: str) -> Embed:
        embed = Embed(
            title=self.__config.HISTORY_TITLE,
            description=description,
            colour=self.__colors.BLUE)
        return embed

    def NOT_PLAYING(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.PLAYER_NOT_PLAYING,
            colour=self.__colors.BLUE)
        return embed

    def QUEUE(self, title: str, description: str) -> Embed:
        embed = Embed(
            title=title,
            description=description,
            colour=self.__colors.BLUE
        )
        return embed

    def INVITE(self, bot_id: str) -> Embed:
        link = self.__config.INVITE_URL
        link.format(bot_id)
        text = self.__config.INVITE_MESSAGE.format(link, link)

        embed = Embed(
            title="Invite Vulkan",
            description=text,
            colour=self.__colors.BLUE
        )
        return embed

    def ERROR_NUMBER(self) -> Embed:
        embed = Embed(
            description=self.__config.ERROR_NUMBER,
            colour=self.__colors.BLACK
        )
        return embed

    def RANDOM_NUMBER(self, a: int, b: int, x: int) -> Embed:
        embed = Embed(
            title=f'Random number between [{a, b}]',
            description=x,
            colour=self.__colors.GREEN
        )
        return embed

    def SONG_REMOVED(self, song_name: str) -> Embed:
        embed = Embed(
            description=self.__config.SONG_REMOVED_SUCCESSFULLY.format(song_name),
            colour=self.__colors.BLUE
        )
        return embed

    def PLAYLIST_RANGE_ERROR(self) -> Embed:
        embed = Embed(
            description=self.__config.LENGTH_ERROR,
            colour=self.__colors.BLACK
        )
        return embed

    def CARA_COROA(self, result: str) -> Embed:
        embed = Embed(
            title='Cara Cora',
            description=f'Result: {result}',
            colour=self.__colors.GREEN
        )
        return embed

    def CHOSEN_THING(self, thing: str) -> Embed:
        embed = Embed(
            title='Choose something',
            description=f'Chosen: {thing}',
            colour=self.__colors.GREEN
        )
        return embed

    def BAD_CHOOSE_USE(self) -> Embed:
        embed = Embed(
            title='Choose something',
            description=f'Error: Use {self.__config.BOT_PREFIX}help choose to understand this command.',
            colour=self.__colors.RED
        )
        return embed
