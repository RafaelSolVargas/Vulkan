import asyncio
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Any, Coroutine, List


class LoopRunner(Thread):
    """
    Class to help deal with asyncio coroutines and loops
    Copyright: https://agariinc.medium.com/advanced-strategies-for-testing-async-code-in-python-6196a032d8d7
    """

    def __init__(self, loop: AbstractEventLoop) -> None:
        # We ensure to always use the same loop
        self.loop = loop
        Thread.__init__(self, name='runner')

    def run(self) -> None:
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_forever()
        finally:
            if self.loop.is_running():
                self.loop.close()

    def run_coroutine(self, coroutine: Coroutine) -> Any:
        """Run a coroutine inside the loop and return the result, doesn't allow concurrency"""
        result = asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        return result.result()

    def _stop(self):
        self.loop.stop()

    def run_in_thread(self, callback, *args):
        return self.loop.call_soon_threadsafe(callback, *args)

    def stop(self):
        return self.run_in_thread(self._stop)

    def run_coroutines_list(self, coroutineList: List[Coroutine]) -> None:
        """Create multiple tasks in the loop and wait for them, use concurrency"""
        tasks = []
        for coroutine in coroutineList:
            tasks.append(self.loop.create_task(coroutine))

        self.run_coroutine(self.__waitForMultipleTasks(tasks))

    async def __waitForMultipleTasks(self, coroutines: List[Coroutine]) -> None:
        """Function to trigger the await for asyncio.wait coroutines"""
        await asyncio.wait(coroutines)
