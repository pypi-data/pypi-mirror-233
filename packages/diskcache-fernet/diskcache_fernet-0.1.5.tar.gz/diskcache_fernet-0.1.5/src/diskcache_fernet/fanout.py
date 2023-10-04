from __future__ import annotations

from os.path import expanduser, expandvars
from pathlib import Path
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Any, Literal, overload

from diskcache import DEFAULT_SETTINGS, Disk, FanoutCache
from typing_extensions import override

from diskcache_fernet.cache import FernetCache
from diskcache_fernet.disk import FernetDisk

__all__ = ["FernetFanoutCache"]


class FernetFanoutCache(FanoutCache):  # noqa: D101
    @override
    def __init__(
        self,
        directory: str | Path | None = None,
        shards: int = 8,
        timeout: float = 60,
        disk: type[Disk] = FernetDisk,
        **settings: Any,
    ) -> None:
        if directory is None:
            directory = mkdtemp(prefix="diskcache-fernet-")
        if isinstance(directory, Path):
            directory = directory.as_posix()
        directory = expanduser(directory)  # noqa: PTH111
        directory = expandvars(directory)
        _dir = Path(directory)

        default_size_limit = DEFAULT_SETTINGS["size_limit"]
        size_limit = settings.pop("size_limit", default_size_limit) / shards

        self._count = shards
        self._directory = directory
        self._disk = disk
        self._shards = tuple(
            FernetCache(
                directory=_dir / f"{num:03d}",
                timeout=timeout,
                disk=disk,
                size_limit=size_limit,
                **settings,
            )
            for num in range(shards)
        )
        self._hash = self._shards[0].disk.hash
        self._caches = {}
        self._deques = {}
        self._indexes = {}

    @property
    def _dir(self) -> Path:
        return self._shards[0]._dir  # noqa: SLF001

    if TYPE_CHECKING:

        @override
        def set(
            self,
            key: Any,
            value: Any,
            expire: float | None = None,
            read: bool = False,  # noqa: FBT001
            tag: str | None = None,
            retry: bool = False,  # noqa: FBT001
        ) -> bool: ...

        @override
        def __setitem__(self, key: Any, value: Any) -> None: ...

        @override
        def add(
            self,
            key: Any,
            value: Any,
            expire: float | None = None,
            read: bool = False,  # noqa: FBT001
            tag: str | None = None,
            retry: bool = False,  # noqa: FBT001
        ) -> bool: ...

        @overload
        def get(
            self,
            key: Any,
            default: Any = ...,
            read: bool = ...,  # noqa: FBT001
            expire_time: Literal[False] = ...,
            tag: Literal[False] = ...,
            retry: bool = ...,  # noqa: FBT001
        ) -> Any: ...

        @overload
        def get(
            self,
            key: Any,
            default: Any = ...,
            read: bool = ...,  # noqa: FBT001
            expire_time: Literal[True] = ...,
            tag: Literal[False] = ...,
            retry: bool = ...,  # noqa: FBT001
        ) -> tuple[Any, float | None]: ...

        @overload
        def get(
            self,
            key: Any,
            default: Any = ...,
            read: bool = ...,  # noqa: FBT001
            expire_time: Literal[False] = ...,
            tag: Literal[True] = ...,
            retry: bool = ...,  # noqa: FBT001
        ) -> tuple[Any, str | None]: ...

        @overload
        def get(
            self,
            key: Any,
            default: Any = ...,
            read: bool = ...,  # noqa: FBT001
            expire_time: Literal[True] = ...,
            tag: Literal[True] = ...,
            retry: bool = ...,  # noqa: FBT001
        ) -> tuple[Any, float | None, str | None]: ...

        @overload
        def get(
            self,
            key: Any,
            default: Any = ...,
            read: bool = ...,  # noqa: FBT001
            expire_time: bool = ...,  # noqa: FBT001
            tag: bool = ...,  # noqa: FBT001
            retry: bool = ...,  # noqa: FBT001
        ) -> Any: ...

        @override
        def get(
            self,
            key: Any,
            default: Any = None,
            read: bool = False,  # noqa: FBT001
            expire_time: bool = False,  # noqa: FBT001
            tag: bool = False,  # noqa: FBT001
            retry: bool = False,  # noqa: FBT001
        ) -> Any: ...

        @override
        def __getitem__(self, key: Any) -> Any: ...


FernetFanoutCache.__doc__ = FanoutCache.__doc__
