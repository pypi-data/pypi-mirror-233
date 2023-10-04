import asyncio
import inspect
import threading
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, cast

from nhs_context_logging import TRACE, log_action


class SingletonProvider:
    def __init__(self):
        self._singletons: dict[Any, Any] = {}
        self._sync_lock: threading.RLock = threading.RLock()
        self._sync_stack: list[Any] = []
        self._async_locks: dict[Any, asyncio.Lock] = {}

    def clear(self, except_keys: tuple[Any, ...] | None = None):
        keys = list(self._singletons.keys())
        for key in keys:
            if except_keys and key in except_keys:
                continue
            del self._singletons[key]
        self._async_locks.clear()
        self._sync_stack.clear()

    @log_action(log_level=TRACE)
    def resolve_sync(self, key, factory: Awaitable[Any] | Callable[[], Any]):
        if key in self._singletons:
            return self._singletons[key]

        with self._sync_lock:
            if key in self._sync_stack:
                raise RecursionError(f"detected recursion resolving {key!r}")

            self._sync_stack.append(key)
            try:
                singleton: Any = (
                    asyncio.run(cast(Coroutine[Any, Any, Any], factory))
                    if inspect.iscoroutinefunction(factory)
                    else cast(Callable[[], Any], factory)()
                )

                self._singletons[key] = singleton

                return singleton
            finally:
                popped = self._sync_stack.pop(-1)
                if popped != key:
                    raise ValueError(f"popped mismatched key {popped!r} expecting {key!r}")

    @log_action(log_level=TRACE)
    async def resolve(self, key, factory: Callable[[], Any]):
        if key in self._singletons:
            return self._singletons[key]

        task = asyncio.current_task()
        assert task
        if not hasattr(task, "resolve_stack"):
            task.resolve_stack = []  # type: ignore[attr-defined]

        resolve_stack: list[Any] = cast(list[Any], task.resolve_stack)  # type: ignore[attr-defined]

        if key in resolve_stack:
            raise RecursionError(f"detected recursion resolving {key!r}")

        resolve_stack.append(key)
        try:
            if key not in self._async_locks:
                with self._sync_lock:
                    if key not in self._async_locks:
                        self._async_locks[key] = asyncio.Lock()

            async with self._async_locks[key]:
                singleton: Any = (
                    await factory() if inspect.iscoroutinefunction(factory) else cast(Callable[[], Any], factory)()
                )

            self._singletons[key] = singleton
        finally:
            popped = resolve_stack.pop(-1)
            if popped != key:
                raise ValueError(f"popped mismatched key {popped!r} expecting {key!r}")

        return singleton


_singletons = SingletonProvider()


def clear(except_keys: tuple[Any, ...] | None = None):
    _singletons.clear(except_keys)


def resolve_sync(key, factory: Awaitable[Any] | Callable[[], Any]):
    return _singletons.resolve_sync(key, factory)


async def resolve(key, factory: Callable[[], Any]):
    return await _singletons.resolve(key, factory)
