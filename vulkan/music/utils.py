import re
import asyncio
from Config.Config import Config
from functools import wraps, partial
config = Config()


def is_connected(ctx):
    try:
        voice_channel = ctx.guild.voice_client.channel

        if not ctx.guild.voice_client.is_connected():
            return None
        else:
            return voice_channel
    except:
        return None


def format_time(duration) -> str:
    if not duration:
        return "00:00"

    hours = duration // 60 // 60
    minutes = duration // 60 % 60
    seconds = duration % 60

    return "{}{}{:02d}:{:02d}".format(
        hours if hours else "",
        ":" if hours else "",
        minutes,
        seconds
    )


def is_url(string) -> bool:
    """Verify if a string is a url"""
    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, string):
        return True
    else:
        return False


class Timer:
    def __init__(self, callback):
        self.__callback = callback
        self.__task = asyncio.create_task(self.__executor())

    async def __executor(self):
        await asyncio.sleep(config.VC_TIMEOUT)
        await self.__callback()

    def cancel(self):
        self.__task.cancel()


def run_async(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        partial_func = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, partial_func)
    return run
