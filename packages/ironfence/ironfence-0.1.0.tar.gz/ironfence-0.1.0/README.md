# IronFence Python Library Documentation

## Introduction

IronFence is a Python library that provides two types of synchronization primitives: Mutex and RWLock. These objects allow you to protect shared data from concurrent access in an asynchronous environment. By using Mutex and RWLock, you can ensure that your application remains coroutine-safe and avoids race conditions[^1].

[^1]: IronFence doesn't protect against inter-process or intra-thread races. Use additional sync mechanisms like [multiprocessing.Lock](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Lock) or [threading.Lock](https://docs.python.org/3/library/threading.html#threading.Lock) for added protection.

## Installation

When pip is available, the distribution can be downloaded from PyPI and installed in one step:

```python
pip install ironfence
```

## Mutex

A `Mutex` (ashort for "mutual exclusion") is a synchronization primitive that allows only one coroutine to access a shared resource at a time. Other coroutines that attempt to acquire the lock will block until the current owner releases it.

```python
import asyncio

import ironfence

shared_state = {}
mu = ironfence.Mutex(shared_state)


async def modify_state():
    print("modifying state..")
    async with mu.lock() as value:
        await asyncio.sleep(1)
        value["key"] = "example"
        print("State modified!")


async def read_state():
    print("reading state..")
    async with mu.lock() as value:
        print("State is:", value)


# run concurrently
asyncio.get_event_loop().run_until_complete(
    asyncio.gather(read_state(), modify_state(), read_state())
)
```

In this example, we create a Mutex instance named `mu` that guards a shared dictionary called `shared_state`. We define two coroutines, `modify_state()` and `read_state()`, that need to access `shared_state`. To ensure exclusive access, we use the `lock()` method of the Mutex object to acquire the lock before modifying or reading the shared data. The `lock()` method returns a context manager that automatically releases the lock when exiting the scope.


## RWLock

An `RWLock` (short for "reader-writer lock") is a synchronization primitive that allows multiple reader coroutines to access a shared resource simultaneously, while allowing only one writer coroutine to modify the resource at a time. This makes it more efficient than a `Mutex` in situations where there are many reader coroutines and only occasional writes.

```python
import asyncio

import ironfence


async def read_state(rw_lock):
    async with rw_lock.read() as value:
        print(value)


async def modify_state(rw_lock):
    async with rw_lock.write() as value:
        value.append("example")


async def main():
    shared_state = []
    rw_lock = ironfence.RWLock(shared_state)
    await asyncio.gather(
        read_state(rw_lock), modify_state(rw_lock), read_state(rw_lock)
    )


asyncio.get_event_loop().run_until_complete(main())
```

In this example, we create an `RWLock` instance named `rw_lock` that guards a shared list called `shared_state`. We define two coroutines, `read_state()` and `modify_state()`, that need to access `shared_state`. To ensure exclusive access, we use the `read()` and `write()` methods of the `RWLock` object to acquire the appropriate locks. The `read()` method acquires a read lock, which allows multiple reader coroutines to enter, while the `write()` method acquires a write lock, which blocks all reader coroutines until the write operation completes.
