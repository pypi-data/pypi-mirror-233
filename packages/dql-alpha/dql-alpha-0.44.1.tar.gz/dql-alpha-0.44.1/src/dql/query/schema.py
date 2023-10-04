import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import getrandbits
from typing import Any, Callable, Dict, Optional

from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.sql.visitors import TraversibleType

from dql.data_storage.abstract import RANDOM_BITS
from dql.dataset import DatasetRow
from dql.node import DirType


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


@dataclass
class TarLocation:
    offset: int
    size: int


class GeneratedRow(ABC):
    """
    Abstract class for creating new rows that will be returned from rows generator
    """

    def __init__(self, name: str, size: int, custom: Dict[str, Any] = None):
        self.name = name
        self.size = size
        self.custom = custom

    @abstractmethod
    def to_dataset_row(self, parent: DatasetRow) -> DatasetRow:
        """
        Method that returns newly generated DatasetRow instance that will
        be added to dataset
        """


class FileRow(GeneratedRow):
    def __init__(
        self,
        name: str,
        size: int,
        custom=None,
        tar_location: TarLocation = None,
    ):
        super().__init__(name, size, custom)
        self.tar_location = tar_location

    @property
    def is_tar_subobject(self):
        return bool(self.tar_location)

    def to_dataset_row(self, parent: DatasetRow):
        parent_dir = parent.path
        name = self.name

        if self.is_tar_subobject:
            full_path = f"{parent.path}/{self.name}"
            parent_dir, name = full_path.rsplit("/", 1)

        row = {
            "id": None,
            # user provided
            "name": name,
            "size": self.size,
            "parent": parent_dir,
            "location": None,
            # inherited from parent
            "vtype": "tar" if self.tar_location else "",  # TODO confirm this
            "dir_type": DirType.FILE,
            "parent_id": parent.id,
            "owner_name": parent.owner_name,
            "owner_id": parent.owner_id,
            "is_latest": parent.is_latest,
            "source": parent.source,
            "last_modified": parent.last_modified,
            # default values
            "version": "",
            "etag": "",
            "checksum": "",
            "anno": None,
            "random": getrandbits(RANDOM_BITS),
        }

        if self.custom:
            # embedding custom columns
            row = {**row, **self.custom}

        if self.is_tar_subobject:
            row["location"] = json.dumps(
                [
                    {
                        "offset": self.tar_location.offset,  # type: ignore [union-attr]
                        "size": self.tar_location.size,  # type: ignore [union-attr]
                        "type": "tar",
                        "parent": parent.path,
                        "etag": parent.etag,
                    },
                ]
            )

        return DatasetRow.from_dict(row)


C = Column
