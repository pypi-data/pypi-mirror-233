from io import IOBase
from typing import Union, Tuple


# multipart file types
NamedFile = Union[
    Tuple[str, IOBase], Tuple[str, IOBase, str]
]  # tuple like ("fname", data, [encoding])
ByteField = Union[bytes, IOBase, NamedFile]
