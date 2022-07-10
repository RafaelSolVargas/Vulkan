import asyncio
from time import time
from typing import Callable, List, Tuple
from Tests.Colors import Colors
from Music.Downloader import Downloader
from Music.Searcher import Searcher
from Tests.TestsHelper import TestsConstants
from Tests.LoopRunner import LoopRunner


class VulkanTesterBase:
    """My own module to execute asyncio tests"""

    def __init__(self) -> None:
        self._downloader = Downloader()
        self._searcher = Searcher()
        self._constants = TestsConstants()
        # Get the list of methods objects of this class if start with test
        self._methodsList: List[Callable] = [getattr(self, func) for func in dir(self) if callable(
            getattr(self, func)) and func.startswith("test")]

    def run(self) -> None:
        self.__printSeparator()
        methodsSummary: List[Tuple[Callable, bool]] = []
        testsSuccessQuant = 0
        testsStartTime = time()

        for method in self._methodsList:
            currentTestStartTime = time()
            self.__printTestStart(method)
            success = False
            try:
                self._setUp()
                success = method()
            except Exception as e:
                success = False
                print(f'ERROR -> {e}')
            finally:
                self._tearDown()

            methodsSummary.append((method, success))
            runTime = time() - currentTestStartTime  # Get the run time of the current test
            if success:
                testsSuccessQuant += 1
                self.__printTestSuccess(method, runTime)
            else:
                self.__printTestFailure(method, runTime)

            self.__printSeparator()

        testsRunTime = time() - testsStartTime
        self.__printTestsSummary(methodsSummary, testsSuccessQuant, testsRunTime)

    def _setUp(self) -> None:
        self._runner = LoopRunner(asyncio.new_event_loop())
        self._runner.start()

    def _tearDown(self) -> None:
        self._runner.stop()
        self._runner.join()

    def __printTestsSummary(self, methods: List[Tuple[Callable, bool]], totalSuccess: int, runTime: int) -> None:
        for index, methodResult in enumerate(methods):
            method = methodResult[0]
            success = methodResult[1]

            if success:
                print(f'{Colors.OKGREEN} {index} -> {method.__name__} = Success {Colors.ENDC}')
            else:
                print(f'{Colors.FAIL} {index} -> {method.__name__} = Failed {Colors.ENDC}')

        print()
        print(
            f'TESTS EXECUTED: {len(methods)} | SUCCESS: {totalSuccess} | FAILED: {len(methods) - totalSuccess} | TIME: {runTime:.2f}sec')

    def __printTestStart(self, method: Callable) -> None:
        print(f'🧪 - Starting {method.__name__}')

    def __printTestSuccess(self, method: Callable, runTime: int) -> None:
        print(f'{method.__name__} -> {Colors.OKGREEN} Success {Colors.ENDC} | ⏰ - {runTime:.2f}sec')

    def __printTestFailure(self, method: Callable, runTime: int) -> None:
        print(f'{method.__name__} -> {Colors.FAIL} Test Failed {Colors.ENDC} | ⏰ - {runTime:.2f}sec')

    def __printSeparator(self) -> None:
        print('=-=' * 15)
