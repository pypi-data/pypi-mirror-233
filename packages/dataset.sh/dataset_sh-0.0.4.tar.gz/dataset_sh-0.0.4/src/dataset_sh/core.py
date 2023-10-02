import time
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from dataset_sh.typing.core import DatasetSchema


class BinaryFile(BaseModel):
    name: str
    source: Optional[str] = None


class DataItemStorageFormat(str, Enum):
    jsonl = 'jsonl'


class CollectionConfig(BaseModel):
    name: str
    data_format: DataItemStorageFormat = DataItemStorageFormat.jsonl
    data_schema: DatasetSchema


class DatasetFileMeta(BaseModel):
    author: Optional[str] = None
    authorEmail: Optional[str] = None
    description: Optional[str] = None
    collections: List[CollectionConfig] = Field(default_factory=list)
    createdAt: int = Field(default_factory=lambda: int(time.time()))

    def find_collection(self, name) -> Optional[CollectionConfig]:
        matched_coll = [c for c in self.collections if c.name == name]
        if len(matched_coll) == 0:
            return None
        return matched_coll[0]
