from discord.ext.commands import Context
from Config.Exceptions import InvalidIndex
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Handlers.JumpMusicHandler import JumpMusicHandler
from Messages.MessagesCategory import MessagesCategory
from UI.Views.BasicView import BasicView
from Utils.Utils import Utils
from Music.VulkanBot import VulkanBot
from Music.Song import Song
from Music.Playlist import Playlist
from typing import List, Union
from discord import Button, Interaction
from UI.Buttons.CallbackButton import CallbackButton
from UI.Buttons.PlaylistDropdown import PlaylistDropdown
from Config.Emojis import VEmojis


class QueueHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, pageNumber=0) -> HandlerResponse:
        # Retrieve the process of the guild
        processManager = self.config.getProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:  # If no process return empty list
            embed = self.embeds.EMPTY_QUEUE()
            return HandlerResponse(self.ctx, embed)

        # Acquire the Lock to manipulate the playlist
        processLock = processInfo.getLock()
        acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        if acquired:
            playlist: Playlist = processInfo.getPlaylist()

            if playlist.isLoopingOne():
                song = playlist.getCurrentSong()
                embed = self.embeds.ONE_SONG_LOOPING(song.info)
                processLock.release()  # Release the Lock
                return HandlerResponse(self.ctx, embed)

            allSongs = playlist.getSongs()
            if len(allSongs) == 0:
                embed = self.embeds.EMPTY_QUEUE()
                processLock.release()  # Release the Lock
                return HandlerResponse(self.ctx, embed)

            songsPages = playlist.getSongsPages()
            if pageNumber < 0 or pageNumber >= len(songsPages):
                embed = self.embeds.INVALID_INDEX()
                error = InvalidIndex()
                processLock.release()  # Release the Lock
                return HandlerResponse(self.ctx, embed, error)

            # Select the page in queue to be printed
            songs = songsPages[pageNumber]
            # Create view for this embed
            buttons = self.__createViewButtons(songsPages, pageNumber)
            buttons.extend(self.__createViewJumpButtons(playlist))
            queueView = BasicView(self.bot, buttons, self.config.QUEUE_VIEW_TIMEOUT)

            if playlist.isLoopingAll():
                title = self.messages.ALL_SONGS_LOOPING
            else:
                title = self.messages.QUEUE_TITLE

            total_time = Utils.format_time(sum([int(song.duration if song.duration else 0)
                                                for song in allSongs]))
            total_songs = len(playlist.getSongs())

            text = f'📜 Queue length: {total_songs} | Page Number: {pageNumber+1}/{len(songsPages)} | ⌛ Duration: `{total_time}` downloaded  \n\n'

            # To work get the correct index of all songs
            startIndex = (pageNumber * self.config.MAX_SONGS_IN_PAGE) + 1
            for pos, song in enumerate(songs, start=startIndex):
                song_name = song.title[:50] if song.title else self.messages.SONG_DOWNLOADING
                text += f"**`{pos}` - ** [{song_name}]({song.identifier}) - `{Utils.format_time(song.duration)}`\n"

            embed = self.embeds.QUEUE(title, text)
            # Release the acquired Lock
            processLock.release()
            return HandlerResponse(self.ctx, embed, view=queueView)
        else:
            processManager.resetProcess(self.guild, self.ctx)
            embed = self.embeds.PLAYER_RESTARTED()
            return HandlerResponse(self.ctx, embed)

    def __createViewButtons(self, songsPages: List[List[Song]], pageNumber: int) -> List[Button]:
        buttons = []
        if pageNumber > 0:
            prevPageNumber = pageNumber - 1
            buttons.append(CallbackButton(self.bot, self.run, VEmojis().BACK, self.ctx.channel,
                                          self.guild.id, MessagesCategory.QUEUE, "Prev Page", pageNumber=prevPageNumber))

        if pageNumber < len(songsPages) - 1:
            nextPageNumber = pageNumber + 1
            buttons.append(CallbackButton(self.bot, self.run, VEmojis().SKIP, self.ctx.channel,
                                          self.guild.id, MessagesCategory.QUEUE, "Next Page", pageNumber=nextPageNumber))

        return buttons

    def __createViewJumpButtons(self, playlist: Playlist) -> List[Button]:
        return [PlaylistDropdown(self.bot, JumpMusicHandler, playlist, self.ctx.channel, self.guild.id, MessagesCategory.PLAYER)]
