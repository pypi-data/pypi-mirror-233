import hashlib
import sys
import tarfile
from functools import partial
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from dql.sql.types import String

from .schema import FileRow, Object, TarLocation
from .udf import udf

if TYPE_CHECKING:
    from dql.catalog import Catalog
    from dql.dataset import DatasetRow


if sys.version_info < (3, 9):
    md5 = hashlib.md5
else:
    md5 = partial(hashlib.md5, usedforsecurity=False)

__all__ = ["index_tar", "checksum"]


def load_tar(raw):
    with tarfile.open(fileobj=raw, mode="r:") as tar:
        return tar.getmembers()


@udf(
    FileRow,
    (Object(load_tar),),
)
def index_tar(tar_entries):
    for info in tar_entries:
        if info.isfile():
            yield FileRow(
                info.name,
                info.size,
                tar_location=TarLocation(info.offset_data, info.size),
            )


BUFSIZE = 2**18


def file_digest(fileobj):
    """Calculate the digest of a file-like object."""
    buf = bytearray(BUFSIZE)  # Reusable buffer to reduce allocations.
    view = memoryview(buf)
    digestobj = md5()
    # From 3.11's hashlib.filedigest()
    while True:
        size = fileobj.readinto(buf)
        if size == 0:
            break  # EOF
        digestobj.update(view[:size])
    return digestobj.hexdigest()


class ChecksumFunc:
    """Calculate checksums for objects reference by dataset rows."""

    output = (("checksum", String),)

    def __init__(self):
        pass

    def __call__(
        self, catalog: "Catalog", row: "DatasetRow"
    ) -> Optional[List[Dict[str, Any]]]:
        with catalog.open_object(row) as f:
            return [{"id": row.id, "checksum": file_digest(f)}]


checksum = ChecksumFunc()
