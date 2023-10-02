import datetime
import os
from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


@dataclass
class DatasetInfo:
    name: str
    is_redirect: bool


class DatasetInfoSnippet(BaseModel):
    datastore: str
    dataset: str
    readme: str


class StoreList(BaseModel):
    stores: List[str]


class DatasetListingResults(BaseModel):
    items: List[DatasetInfoSnippet]


class SourceInfo(BaseModel):
    url: str
    download_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class DatasetHomeFolderFilenames:
    MARKER = '.dataset.marker'
    META = 'meta.json'
    DATA_FILE = 'file'
    README = 'readme.md'
    REMOTE_SOURCE = 'remote_source.json'  # if this file is downloaded from a remote source,


class DatasetFileInternalPath:
    BINARY_FOLDER = 'bin'
    COLLECTION_FOLDER = 'coll'

    META_FILE_NAME = 'meta.json'
    DATA_FILE = 'data.jsonl'


@dataclass
class DatasetHomeFolder:
    base: str
    name: Optional[str] = None

    def meta(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.META)

    def marker(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.MARKER)

    def datafile(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.DATA_FILE)

    def readme(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.README)

    def marker_exist(self):
        return os.path.isfile(self.marker())

    def remote_source(self):
        return os.path.join(self.base, DatasetHomeFolderFilenames.REMOTE_SOURCE)

    def code_example(self, collection_name):
        return os.path.join(self.base, f'usage_code_{collection_name}.py')

    def sample_file(self, collection_name):
        return os.path.join(self.base, f'data_sample_{collection_name}.jsonl')
