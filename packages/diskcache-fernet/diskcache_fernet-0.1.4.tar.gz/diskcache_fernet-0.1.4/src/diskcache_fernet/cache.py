from __future__ import annotations

from errno import EEXIST
from functools import cached_property
from os.path import expanduser, expandvars
from pathlib import Path
from sqlite3 import OperationalError
from tempfile import mkdtemp
from threading import local
from typing import TYPE_CHECKING, Any, Literal, overload

from cryptography.fernet import Fernet
from diskcache import DEFAULT_SETTINGS, Cache, Disk
from diskcache.core import EVICTION_POLICY, METADATA
from typing_extensions import override

from diskcache_fernet.disk import FernetDisk
from diskcache_fernet.secret import SecretValue

__all__ = ["FernetCache"]


class FernetCache(Cache):  # noqa: D101
    @override
    def __init__(
        self,
        directory: str | Path | None = None,
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
        self._directory = directory
        self._timeout = 0
        self._local = local()
        self._txn_id = None

        if not self._dir.is_dir():
            try:
                self._dir.mkdir(mode=0o755, exist_ok=False)
            except OSError as exc:
                if exc.errno != EEXIST:
                    error_msg = (
                        f"cache dir {self._dir!s} does not exist"
                        " and could not be created"
                    )
                    raise OSError(exc.errno, error_msg) from exc

        self._setup(timeout=timeout, disk=disk, **settings)

    @cached_property
    def _dir(self) -> Path:
        return Path(self._directory)

    def _setup(self, timeout: float, disk: type[Disk], **settings: Any) -> None:
        """obtained from diskcache.core.Cache.__init__"""
        sql = self._sql_retry

        # Setup Settings table.

        try:
            current_settings = dict(
                sql("SELECT key, value FROM Settings").fetchall(),
            )
        except OperationalError:
            current_settings = {}

        sets = DEFAULT_SETTINGS.copy()
        sets.update(current_settings)
        sets.update(settings)

        for key in METADATA:
            sets.pop(key, None)

        # Chance to set pragmas before any tables are created.

        for key, value in sorted(sets.items()):
            if key.startswith("sqlite_"):
                self.reset(key, value, update=False)

        sql(
            "CREATE TABLE IF NOT EXISTS Settings ( key TEXT NOT NULL UNIQUE, value)",
        )

        # Setup Disk object (must happen after settings initialized).

        kwargs = {
            key[5:]: value for key, value in sets.items() if key.startswith("disk_")
        }
        self._disk = disk(self._directory, **kwargs)

        # Set cached attributes: updates settings and sets pragmas.

        for key, value in sets.items():
            if isinstance(value, (SecretValue, Fernet)):
                continue
            query = "INSERT OR REPLACE INTO Settings VALUES (?, ?)"
            sql(query, (key, value))
            self.reset(key, value)

        for key, value in METADATA.items():
            query = "INSERT OR IGNORE INTO Settings VALUES (?, ?)"
            sql(query, (key, value))
            self.reset(key)

        ((self._page_size,),) = sql("PRAGMA page_size").fetchall()

        # Setup Cache table.

        sql(
            "CREATE TABLE IF NOT EXISTS Cache ("
            " rowid INTEGER PRIMARY KEY,"
            " key BLOB,"
            " raw INTEGER,"
            " store_time REAL,"
            " expire_time REAL,"
            " access_time REAL,"
            " access_count INTEGER DEFAULT 0,"
            " tag BLOB,"
            " size INTEGER DEFAULT 0,"
            " mode INTEGER DEFAULT 0,"
            " filename TEXT,"
            " value BLOB)",
        )

        sql(
            "CREATE UNIQUE INDEX IF NOT EXISTS Cache_key_raw ON Cache(key, raw)",
        )

        sql(
            "CREATE INDEX IF NOT EXISTS Cache_expire_time ON Cache (expire_time)",
        )

        query = EVICTION_POLICY[self.eviction_policy]["init"]  # type: ignore

        if query is not None:
            sql(query)

        # Use triggers to keep Metadata updated.

        sql(
            "CREATE TRIGGER IF NOT EXISTS Settings_count_insert"
            " AFTER INSERT ON Cache FOR EACH ROW BEGIN"
            " UPDATE Settings SET value = value + 1"
            ' WHERE key = "count"; END',
        )

        sql(
            "CREATE TRIGGER IF NOT EXISTS Settings_count_delete"
            " AFTER DELETE ON Cache FOR EACH ROW BEGIN"
            " UPDATE Settings SET value = value - 1"
            ' WHERE key = "count"; END',
        )

        sql(
            "CREATE TRIGGER IF NOT EXISTS Settings_size_insert"
            " AFTER INSERT ON Cache FOR EACH ROW BEGIN"
            " UPDATE Settings SET value = value + NEW.size"
            ' WHERE key = "size"; END',
        )

        sql(
            "CREATE TRIGGER IF NOT EXISTS Settings_size_update"
            " AFTER UPDATE ON Cache FOR EACH ROW BEGIN"
            " UPDATE Settings"
            " SET value = value + NEW.size - OLD.size"
            ' WHERE key = "size"; END',
        )

        sql(
            "CREATE TRIGGER IF NOT EXISTS Settings_size_delete"
            " AFTER DELETE ON Cache FOR EACH ROW BEGIN"
            " UPDATE Settings SET value = value - OLD.size"
            ' WHERE key = "size"; END',
        )

        # Create tag index if requested.

        if self.tag_index:  # type: ignore
            self.create_tag_index()
        else:
            self.drop_tag_index()

        # Close and re-open database connection with given timeout.

        self.close()
        self._timeout = timeout
        self._sql  # noqa: B018

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


FernetCache.__doc__ = Cache.__doc__
