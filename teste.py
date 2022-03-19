from vulkan.music.Downloader import Downloader
from vulkan.music.Playlist import Playlist
from vulkan.music.Song import Song
import asyncio
from yt_dlp import YoutubeDL
from vulkan.music.Types import Provider

# Link pego de mix
link1 = 'https://youtu.be/5w61TizfZXY?list=RDMM5w61TizfZXY'
# Video especifico
link2 = 'https://www.youtube.com/watch?v=WFEtDqLLv84&ab_channel=MMAK'
# Link pego de mix
link3 = 'https://www.youtube.com/watch?v=5w61TizfZXY&list=RDMM5w61TizfZXY&ab_channel=CantusFidei'
# Playlist
link4 = 'https://www.youtube.com/playlist?list=PLbbKJHHZR9SgWK6SBOwnTaaQauvhjJaNE'
# Nome
link5 = 'Rumbling'

down = Downloader()
playlist = Playlist()


__YDL_OPTIONS = {'format': 'bestaudio/best',
                 'default_search': 'auto',
                 'playliststart': 0,
                 'extract_flat': True,
                 'playlistend': 5,
                 'noplaylist': True
                 }


async def main():
    down = Downloader()
    link = 'https://youtu.be/5w61TizfZXY?list=RDMM5w61TizfZXY'

    infos = await down.extract_info('Rumbling')
    song = playlist.add_song('Rumbling', 'Rafael')
    await down.preload([song])
    print(song.source)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
