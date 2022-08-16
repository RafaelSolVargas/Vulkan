from typing import List
from discord import Button, TextChannel
from discord.ui import View
from Config.Emojis import VEmojis
from Messages.MessagesCategory import MessagesCategory
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessInfo import ProcessInfo
from Config.Messages import Messages
from Music.Song import Song
from Config.Embeds import VEmbeds
from UI.Buttons.HandlerButton import HandlerButton
from UI.Views.BasicView import BasicView
from Messages.MessagesManager import MessagesManager
from Handlers.PrevHandler import PrevHandler
from Handlers.PauseHandler import PauseHandler
from Handlers.SkipHandler import SkipHandler
from Handlers.StopHandler import StopHandler
from Handlers.ResumeHandler import ResumeHandler
from Handlers.LoopHandler import LoopHandler
from Handlers.QueueHandler import QueueHandler


class ProcessCommandsExecutor:
    def __init__(self, bot: VulkanBot, guildID: int) -> None:
        self.__bot = bot
        self.__guildID = guildID
        self.__messagesManager = MessagesManager()
        self.__messages = Messages()
        self.__embeds = VEmbeds()
        self.__emojis = VEmojis()

    async def sendNowPlaying(self, processInfo: ProcessInfo, song: Song) -> None:
        # Get the lock of the playlist
        playlist = processInfo.getPlaylist()
        if playlist.isLoopingOne():
            title = self.__messages.ONE_SONG_LOOPING
        else:
            title = self.__messages.SONG_PLAYING

        # Create View and Embed
        embed = self.__embeds.SONG_INFO(song.info, title)
        channel = processInfo.getTextChannel()
        view = self.__getPlayerView(channel)
        # Send Message and add to the MessagesManager
        message = await channel.send(embed=embed, view=view)
        await self.__messagesManager.addMessageAndClearPrevious(self.__guildID, MessagesCategory.NOW_PLAYING, message, view)

        # Set in the view the message witch contains the view
        view.set_message(message=message)

    def __getPlayerView(self, channel: TextChannel) -> View:
        buttons = self.__getPlayerButtons(channel)
        view = BasicView(self.__bot, buttons)
        return view

    def __getPlayerButtons(self, textChannel: TextChannel) -> List[Button]:
        """Create the Buttons to be inserted in the Player View"""
        buttons: List[Button] = []

        buttons.append(HandlerButton(self.__bot, PrevHandler, self.__emojis.BACK,
                                     textChannel, self.__guildID, MessagesCategory.PLAYER, "Back"))
        buttons.append(HandlerButton(self.__bot, PauseHandler, self.__emojis.PAUSE,
                                     textChannel, self.__guildID, MessagesCategory.PLAYER, "Pause"))
        buttons.append(HandlerButton(self.__bot, ResumeHandler, self.__emojis.PLAY,
                                     textChannel, self.__guildID, MessagesCategory.PLAYER, "Play"))
        buttons.append(HandlerButton(self.__bot, StopHandler, self.__emojis.STOP,
                                     textChannel, self.__guildID, MessagesCategory.PLAYER, "Stop"))
        buttons.append(HandlerButton(self.__bot, SkipHandler, self.__emojis.SKIP,
                                     textChannel, self.__guildID, MessagesCategory.PLAYER, "Skip"))
        buttons.append(HandlerButton(self.__bot, QueueHandler, self.__emojis.QUEUE,
                                     textChannel, self.__guildID, MessagesCategory.QUEUE, "Songs"))
        buttons.append(HandlerButton(self.__bot, LoopHandler, self.__emojis.LOOP_ONE,
                                     textChannel, self.__guildID, MessagesCategory.LOOP, "Loop One", 'One'))
        buttons.append(HandlerButton(self.__bot, LoopHandler, self.__emojis.LOOP_OFF,
                                     textChannel, self.__guildID, MessagesCategory.LOOP, "Loop Off", 'Off'))
        buttons.append(HandlerButton(self.__bot, LoopHandler, self.__emojis.LOOP_ALL,
                                     textChannel, self.__guildID, MessagesCategory.LOOP, "Loop All", 'All'))

        return buttons
