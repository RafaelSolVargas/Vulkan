import asyncio
from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Music.Downloader import Downloader
from Utils.Utils import Utils
from Parallelism.ProcessManager import ProcessManager


class QueueHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__down = Downloader()

    async def run(self) -> HandlerResponse:
        # Retrieve the process of the guild
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:  # If no process return empty list
            embed = self.embeds.EMPTY_QUEUE()
            return HandlerResponse(self.ctx, embed)

        # Acquire the Lock to manipulate the playlist
        processLock = processInfo.getLock()
        acquired = processLock.acquire(timeout=self.config.ACQUIRE_LOCK_TIMEOUT)
        if acquired:
            playlist = processInfo.getPlaylist()

            if playlist.isLoopingOne():
                song = playlist.getCurrentSong()
                embed = self.embeds.ONE_SONG_LOOPING(song.info)
                return HandlerResponse(self.ctx, embed)

            songs_preload = playlist.getSongsToPreload()
            allSongs = playlist.getSongs()
            if len(songs_preload) == 0:
                embed = self.embeds.EMPTY_QUEUE()
                return HandlerResponse(self.ctx, embed)

            asyncio.create_task(self.__down.preload(songs_preload))

            if playlist.isLoopingAll():
                title = self.messages.ALL_SONGS_LOOPING
            else:
                title = self.messages.QUEUE_TITLE

            total_time = Utils.format_time(sum([int(song.duration if song.duration else 0)
                                                for song in allSongs]))
            total_songs = len(playlist.getSongs())

            text = f'📜 Queue length: {total_songs} | ⌛ Duration: `{total_time}` downloaded  \n\n'

            for pos, song in enumerate(songs_preload, start=1):
                song_name = song.title if song.title else self.messages.SONG_DOWNLOADING
                text += f"**`{pos}` - ** {song_name} - `{Utils.format_time(song.duration)}`\n"

            embed = self.embeds.QUEUE(title, text)
            # Release the acquired Lock
            processLock.release()
            return HandlerResponse(self.ctx, embed)
        else:
            processManager.resetProcess(self.guild, self.ctx)
            embed = self.embeds.PLAYER_RESTARTED()
            return HandlerResponse(self.ctx, embed)
