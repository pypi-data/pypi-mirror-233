# diskcache-fernet

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![github action](https://github.com/phi-friday/diskcache-fernet/actions/workflows/check.yaml/badge.svg?event=push&branch=main)](#)
[![PyPI version](https://badge.fury.io/py/diskcache-fernet.svg)](https://badge.fury.io/py/diskcache-fernet)
[![python version](https://img.shields.io/pypi/pyversions/diskcache-fernet.svg)](#)

## how to install
```shell
$ pip install diskcache-fernet
```

## how to use
```python
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from diskcache import Cache

from diskcache_fernet import FernetDisk


def main(temp: Path) -> None:
    origin = Cache(temp)
    fernet = Cache(temp, disk=FernetDisk)
    # or add fernet key
    # fernet = Cache(temp, disk=FernetDisk, disk_fernet=b"some fernet key")

    fernet["key"] = "value"

    from_fernet = fernet["key"]
    from_origin = origin["key"]

    assert from_fernet != from_origin
    assert from_fernet == "value"

    print(from_origin)
    # like:
    # gAAAAABlGtPWAPEcYLqu6waiUd551H4jfAvQlulWnfwyWTVtjZyF6AkUCVFQKPpIRz9vu29y1FoduIYoK-mOz5CJt0Kx-pv2zQ==


if __name__ == "__main__":
    with TemporaryDirectory() as temp:
        main(Path(temp))
```

## License

Apache-2.0, see [LICENSE](https://github.com/phi-friday/diskcache-fernet/blob/main/LICENSE).