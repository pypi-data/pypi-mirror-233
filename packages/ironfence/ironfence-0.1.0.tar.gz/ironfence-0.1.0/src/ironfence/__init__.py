import asyncio
import contextlib
from dataclasses import InitVar, dataclass
from typing import Any, AsyncGenerator, Generic, TypeVar

import aiorwlock

__version__ = "0.1.0"

T = TypeVar("T")


@dataclass
class Primitive(Generic[T]):
    value: InitVar[Any]

    __slots__ = "__value", "__lock", "value"


@dataclass
class Mutex(Primitive[T]):
    """
    Mutual Exclusion mechanism, which ensures that at most coroutine at a time is able
    to access some data.

    .. note::
        The mutex is implemented using an instance of `asyncio.Lock`_, which provides
        efficient and lightweight synchronization for asynchronous code.

        .. _asyncio.Lock: https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock
    """

    def __post_init__(self, value: T) -> None:
        self.__value = value
        self.__lock = asyncio.Lock()

    @contextlib.asynccontextmanager
    async def lock(self) -> AsyncGenerator["T", None]:
        await self.__lock.acquire()
        try:
            yield self.__value
        finally:
            self.__lock.release()


@dataclass
class RWLock(Primitive[T]):
    """
    Provides a mutual exclusion mechanism which allows multiple readers at the same
    time, while allowing only one writer at a time. In some cases, this can be more
    efficient than a mutex.

    The `fast` parameter controls whether the lock will automatically switch contexts
    when it is acquired. By default, the lock will switch contexts, allowing other
    waiting tasks to acquire the lock even if the current holder does not contain
    context switches (e.g., await, async with, async for, or yield from statements).

    Setting `fast=True` disables context switching, which can provide a minor speedup in
    situations where the locked code contains context switches. However, it is important
    to note that disabling context switching can also lead to poorer performance in
    certain scenarios, as other waiting tasks may be unable to acquire the lock until
    the current holder releases it.

    It is recommended to carefully consider the requirements of your application before
    setting `fast=True`. If you are unsure whether to enable context switching, leave
    the `fast` parameter unset or set it to `False`, which is the default and safest
    option.

    .. note::
        The RWLock is implemented using an instance of `aiorwlock.RWLock`_, which
        provides efficient and lightweight synchronization for asynchronous code.

        .. _aiorwlock.RWLock:: https://github.com/aio-libs/aiorwlock#aiorwlock
    """

    value: InitVar[T]
    fast: InitVar[bool] = False

    def __post_init__(self, value: T, fast: bool) -> None:
        self.__value = value
        self.__lock = aiorwlock.RWLock(fast=fast)

    @contextlib.asynccontextmanager
    async def read(self) -> AsyncGenerator["T", None]:
        await self.__lock.reader.acquire()
        try:
            yield self.__value
        finally:
            self.__lock.reader.release()

    @contextlib.asynccontextmanager
    async def write(self) -> AsyncGenerator["T", None]:
        await self.__lock.writer.acquire()
        try:
            yield self.__value
        finally:
            self.__lock.writer.release()


__all__ = "Primitive", "RWLock", "Mutex"
