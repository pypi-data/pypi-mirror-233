from __future__ import annotations

import pickle
from functools import cached_property
from io import BytesIO, FileIO, StringIO
from pathlib import Path
from sqlite3 import Binary
from typing import Any

from cryptography.fernet import Fernet
from diskcache import UNKNOWN, Disk
from diskcache.core import MODE_BINARY, MODE_PICKLE, MODE_RAW, MODE_TEXT
from typing_extensions import override

from diskcache_fernet.log import logger
from diskcache_fernet.secret import SecretValue


class FernetDisk(Disk):  # noqa: D101
    @override
    def __init__(
        self,
        directory: str | Path,
        min_file_size: int = 0,
        pickle_protocol: int = 0,
        fernet: str
        | bytes
        | SecretValue[str]
        | SecretValue[bytes]
        | Fernet
        | None = None,
    ) -> None:
        if isinstance(directory, Path):
            directory = directory.as_posix()
        super().__init__(directory, min_file_size, pickle_protocol)

        if fernet is None:
            logger.warning(
                "there is no fernet in settings. "
                "A temporary fernet key will be generated.",
            )
            fernet = Fernet(Fernet.generate_key())

        if isinstance(fernet, SecretValue):
            fernet = Fernet(fernet.get_value())
        elif not isinstance(fernet, Fernet):
            logger.warning("fernet key is not secret value.")
            fernet = Fernet(fernet)

        self._fernet = fernet

    @cached_property
    def _dir(self) -> Path:
        return Path(self._directory).resolve()

    @override
    def filename(self, key: Any = UNKNOWN, value: Any = UNKNOWN) -> tuple[str, str]:
        return super().filename(key, value)

    @override
    def store(
        self,
        value: Any,
        read: bool,  # noqa: FBT001
        key: Any = UNKNOWN,
    ) -> tuple[int, int, str | None, Binary | None]:
        if isinstance(value, FileIO):
            if not read:
                raise TypeError("value is file io but read=False")
            value = value.read()

        if isinstance(value, bytes):
            value = self._encrypt(value)

            if len(value) < self.min_file_size:
                return 0, MODE_RAW, None, Binary(value)

            filename, full_path = self.filename(key, value)
            self._write(full_path, BytesIO(value), "xb")
            return len(value), MODE_BINARY, filename, None

        if isinstance(value, str):
            value = self._encrypt(value.encode("utf-8")).decode("utf-8")

            filename, full_path = self.filename(key, value)
            self._write(full_path, StringIO(value), "x", "UTF-8")
            size = Path(full_path).stat().st_size
            return size, MODE_TEXT, filename, None

        result = pickle.dumps(value, protocol=self.pickle_protocol)
        safe = self._encrypt(result)
        length = len(safe)

        if length < self.min_file_size:
            return 0, MODE_PICKLE, None, Binary(safe)

        filename, full_path = self.filename(key, value)
        self._write(full_path, BytesIO(safe), "xb")
        return length, MODE_PICKLE, filename, None

    @override
    def fetch(
        self,
        mode: int,
        filename: str | None,
        value: Any,
        read: bool,  # noqa: FBT001
    ) -> Any:
        if mode == MODE_RAW:
            safe = bytes(value) if isinstance(value, Binary) else value
            return self._decrypt(safe)

        file = self._dir if filename is None else self._dir / filename
        if mode == MODE_BINARY:
            if read:
                return file.open("rb")

            with file.open("rb") as reader:
                safe = reader.read()
                return self._decrypt(safe)

        if mode == MODE_TEXT:
            with file.open("r", encoding="utf-8") as reader:
                safe = reader.read()
                return self._decrypt(safe.encode("utf-8")).decode("utf-8")

        if mode == MODE_PICKLE and value is None:
            with file.open("rb") as reader:
                safe = reader.read()
                safe_pickable = self._decrypt(safe)
                return pickle.load(BytesIO(safe_pickable))  # noqa: S301

        safe_pickable = self._decrypt(value)
        return pickle.load(BytesIO(safe_pickable))  # noqa: S301

    def _encrypt(self, value: bytes) -> bytes:
        return self._fernet.encrypt(value)

    def _decrypt(self, value: bytes) -> bytes:
        return self._fernet.decrypt(value)

    @property
    def _token(self) -> SecretValue[bytes]:
        return SecretValue(
            self._fernet._signing_key + self._fernet._encryption_key,  # noqa: SLF001
        )


FernetDisk.__doc__ = Disk.__doc__
