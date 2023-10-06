import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Tuple

from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.sql.visitors import TraversibleType

from dql.sql.types import JSON, Boolean, Int, String


class ColumnMeta(TraversibleType):
    def __getattr__(cls, name: str):  # noqa: B902
        return cls(name)  # pylint: disable=no-value-for-parameter


class Object:
    """
    Object is used as a placeholder parameter to indicate the actual stored object
    being passed as a parameter to the UDF.
    """

    def __init__(self, reader: Callable, cache: bool = False):
        """
        Initialize the object and specify the reader to be
        used for loading the object into memory.
        """
        self.reader = reader
        self.cache = cache


class LocalFilename:
    """
    Placeholder parameter representing the local path to a cached copy of the object.
    """


class Column(ColumnClause, metaclass=ColumnMeta):  # pylint: disable=abstract-method
    inherit_cache: Optional[bool] = True

    def __init__(self, text, type_=None, is_literal=False, _selectable=None):
        self.name = text
        super().__init__(
            text, type_=type_, is_literal=is_literal, _selectable=_selectable
        )

    def glob(self, glob_str):
        return self.op("GLOB")(glob_str)


class DatasetRow:
    schema = (
        ("name", String),
        ("size", Int),
        ("parent", String),
        ("location", JSON),
        ("vtype", String),
        ("dir_type", String),
        ("owner_name", String),
        ("owner_id", String),
        ("is_latest", Boolean),
        ("last_modified", datetime),
        ("version", String),
        ("etag", String),
        ("checksum", String),
        ("anno", JSON),
    )

    @staticmethod
    def create(
        name: str,
        size: int = 0,
        parent: str = "",
        location: Dict[str, Any] = None,
        vtype: str = "",
        dir_type: int = 0,
        owner_name: str = "",
        owner_id: str = "",
        is_latest: bool = True,
        last_modified: datetime = None,
        version: str = "",
        etag: str = "",
        checksum: str = "",
        anno: Dict[str, Any] = None,
    ) -> Tuple[
        str,
        int,
        str,
        Optional[str],
        str,
        int,
        str,
        str,
        bool,
        datetime,
        str,
        str,
        str,
        Optional[str],
    ]:
        if location:
            location = json.dumps([location])  # type: ignore [assignment]

        if anno:
            anno = json.dumps(anno)  # type: ignore [assignment]

        last_modified = last_modified or datetime.now(timezone.utc)

        return (  # type: ignore [return-value]
            name,
            size,
            parent,
            location,
            vtype,
            dir_type,
            owner_name,
            owner_id,
            is_latest,
            last_modified,
            version,
            etag,
            checksum,
            anno,
        )


C = Column
