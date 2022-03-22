from discord import Embed
from Config.Config import Config
from Config.Colors import Colors
from datetime import timedelta


class Embeds:
    def __init__(self) -> None:
        self.__config = Config()
        self.__colors = Colors()

    @property
    def INVALID_INPUT(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.INVALID_INPUT,
            colours=self.__colors.BLUE)
        return embed

    @property
    def UNAVAILABLE_VIDEO(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.VIDEO_UNAVAILABLE,
            colours=self.__colors.BLUE)
        return embed

    @property
    def DOWNLOADING_ERROR(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.DOWNLOADING_ERROR,
            colours=self.__colors.BLUE)
        return embed

    @property
    def SONG_ADDED(self, title: str) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONG_ADDED.format(title),
            colours=self.__colors.BLUE)
        return embed

    @property
    def SONGS_ADDED(self, quant: int) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.SONGS_ADDED.format(quant),
            colour=self.__colors.BLUE)
        return embed

    @property
    def SONG_INFO(self, info: dict, title: str, position='Playing Now') -> Embed:
        embedvc = Embed(
            title=title,
            description=f"[{info['title']}]({info['original_url']})",
            color=self.__config.COLOURS['blue']
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

    @property
    def COMMAND_ERROR(self):
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.ERROR_MISSING_ARGUMENTS,
            colour=self.__colors.BLACK
        )
        return embed

    @property
    def COMMAND_NOT_FOUND(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.COMMAND_NOT_FOUND,
            colour=self.__colors.BLACK
        )
        return embed

    @property
    def MY_ERROR_BAD_COMMAND(self) -> Embed:
        embed = Embed(
            title=self.__config.BAD_COMMAND_TITLE,
            description=self.__config.BAD_COMMAND,
            colour=self.__colors.BLACK
        )
        return embed

    @property
    def UNKNOWN_ERROR(self) -> Embed:
        embed = Embed(
            title=self.__config.ERROR_TITLE,
            description=self.__config.UNKNOWN_ERROR,
            colour=self.__colors.RED
        )
        return embed

    @property
    def FAIL_DUE_TO_LOOP_ON(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.LOOP_ON,
            colour=self.__colors.BLUE
        )
        return embed

    @property
    def NOT_PREVIOUS_SONG(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.NOT_PREVIOUS,
            colour=self.__colors.BLUE
        )
        return embed

    @property
    def HISTORY(self, description: str) -> Embed:
        embed = Embed(
            title=self.__config.HISTORY_TITLE,
            description=description,
            colour=self.__colors.BLUE)
        return embed

    @property
    def NOT_PLAYING(self) -> Embed:
        embed = Embed(
            title=self.__config.SONG_PLAYER,
            description=self.__config.PLAYER_NOT_PLAYING,
            colour=self.__colors.BLUE)
        return embed

    @property
    def QUEUE(self, title: str, description: str) -> Embed:
        embed = Embed(
            title=title,
            description=description,
            colour=self.__colors.BLUE
        )
        return embed

    @property
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

    @property
    def ERROR_NUMBER(self) -> Embed:
        embed = Embed(
            description=self.__config.ERROR_NUMBER,
            colour=self.__colors.RED
        )
        return embed

    @property
    def RANDOM_NUMBER(self, a: int, b: int, x: int) -> Embed:
        embed = Embed(
            title=f'Random number between [{a, b}]',
            description=x,
            colour=self.__colors.GREEN
        )
        return embed

    @property
    def CARA_COROA(self, result: str) -> Embed:
        embed = Embed(
            title='Cara Cora',
            description=f'Result: {result}',
            colour=self.__colors.GREEN
        )
        return embed

    @property
    def CHOSEN_THING(self, thing: str) -> Embed:
        embed = Embed(
            title='Choose something',
            description=f'Chosen: {thing}',
            colour=self.__config.COLOURS['green']
        )
        return embed

    @property
    def BAD_CHOOSE_USE(self) -> Embed:
        embed = Embed(
            title='Choose something',
            description=f'Error: Use {self.__config.BOT_PREFIX}help choose to understand this command.',
            colour=self.__colors.RED
        )
        return embed
