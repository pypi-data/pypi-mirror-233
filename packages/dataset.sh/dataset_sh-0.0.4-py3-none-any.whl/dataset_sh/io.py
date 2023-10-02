import json
import os
import shutil
import tempfile
import time
import urllib
import urllib.request
import uuid
import warnings
import zipfile
from typing import Optional, Type, TypeVar, List
from urllib.error import HTTPError

from pydantic import BaseModel

from .config import get_storage_base_folder
from .models import DatasetInfoSnippet, StoreList, DatasetListingResults, DatasetHomeFolder, \
    SourceInfo, DatasetFileInternalPath
from .typing.codegen import CodeGenerator
from .typing.schema_builder import SchemaBuilder
from .utils.misc import readfile_or_default, is_name_legit, parse_dataset_name, read_jsonl, try_parse_error
from .core import CollectionConfig, DatasetFileMeta

DataModel = TypeVar('DataModel', bound=BaseModel)


class DatasetFile:

    def __init__(self):
        raise ValueError('Please use DatasetFile.open(filename, mode)')

    @staticmethod
    def open(fp: str, mode: str = 'r'):
        """
        Open a dataset file
        :param fp: path to the file
        :param mode: r for read and w for write.
        :return:
        """
        if mode == 'r':
            return DatasetFileReader(fp)
        elif mode == 'w':
            return DatasetFileWriter(fp)
        else:
            raise ValueError('mode must be one of "r" or "w"')

    @staticmethod
    def binary_file_path(fn: str):
        return os.path.join(DatasetFileInternalPath.BINARY_FOLDER, fn)


class DatasetFileWriter:
    def __init__(self, file_path: str):
        """
        Write to a dataset file, this object can also be used as a context manager.

        This object need to be closed.

        :param file_path: location of the dataset file to write.
        """
        self.zip_file = zipfile.ZipFile(file_path, 'w')
        self.meta = DatasetFileMeta()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        close the writer.
        :return:
        """
        self.meta.createdAt = int(time.time())
        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'w') as out:
            out.write(self.meta.model_dump_json().encode('utf-8'))
        self.zip_file.close()

    def add_collection(
            self,
            collection_name: str,
            data: List,
            model: Optional[Type[DataModel]] = None,
    ):
        """
        add a data collection to this dataset.
        :param collection_name: name of the collection to add.
        :param data: list of objects that extends pydantic BaseModel.
        :param model: the pydantic model class.
        :return:
        """
        for coll in self.meta.collections:
            if coll.name == collection_name:
                raise ValueError(f'collection {collection_name} already exists')

        if model is None:
            if isinstance(data[0], BaseModel):
                warnings.warn(f'model class is not provided, using {data[0].__class__.__name__} as model')
                model = data[0].__class__
            else:
                raise ValueError('Input data must be pydantic model')

        dataset_schema = SchemaBuilder.build(model)

        new_coll = CollectionConfig(
            name=collection_name,
            data_schema=dataset_schema,
        )

        self.meta.collections.append(new_coll)
        target_fp = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(target_fp, 'w') as out:
            for item in data:
                out.write(item.model_dump_json(round_trip=True).encode('utf-8'))
                out.write("\n".encode('utf-8'))

    def add_binary_file(self, fn: str, content: bytes):
        """
        Add a binary file to the dataset
        :param fn: name of the binary file.
        :param content: content in bytes.
        :return:
        """
        binary_file_path = DatasetFile.binary_file_path(fn)
        with self.zip_file.open(binary_file_path, 'w') as out:
            out.write(content)


class DatasetFileReader:
    def __init__(self, file_path):
        """
        Read a dataset, this object can be used as a context manager.

        This object must be closed.

        :param file_path:
        """
        self.zip_file = zipfile.ZipFile(file_path, 'r')

        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'r') as fd:
            self.meta = DatasetFileMeta(**json.load(fd))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.zip_file.close()

    def binary_files(self):
        """
        Open a binary file for read.
        :return: a file descriptor for the binary file to read.
        """
        prefix = DatasetFileInternalPath.BINARY_FOLDER + '/'
        for name in self.zip_file.namelist():
            if name.startswith(prefix):
                yield name[len(prefix):]

    def open_binary_file(self, filename):
        """
        Open a binary file for read.
        :param filename: name of the binary file.
        :return: a file descriptor for the binary file to read.
        """
        return self.zip_file.open(
            DatasetFile.binary_file_path(filename),
            'r'
        )

    def collection(self, collection_name, model=None):
        """
        Open a collection.
        :param collection_name: name of a collection
        :param model: an optional pydantic model class to hold the data.
        :return: a CollectionReader object for the given collection name.
        """
        cfg = [c for c in self.meta.collections if c.name == collection_name]
        if len(cfg) == 0:
            raise ValueError(f"Collection {collection_name} do not exist")
        else:
            cfg = cfg[0]
        return CollectionReader(self.zip_file, collection_name, cfg, model=model)

    def coll(self, collection_name, model=None):
        return self.collection(collection_name, model=model)

    def collections(self):
        """
        List all collection names
        :return: list of collection names.
        """
        return [c.name for c in self.meta.collections]

    def __getitem__(self, item):
        return self.collection(item)


class CollectionReader(object):
    def __init__(self, zip_file, collection_name, config: CollectionConfig, model=None):
        """
        Collection Reader
        :param zip_file:
        :param collection_name:
        :param config:
        :param model:
        """
        self.zip_file = zip_file
        self.collection_name = collection_name
        self.config = config
        self.model = model

    def code_usage(self):
        generator = CodeGenerator()
        code = generator.generate_all(self.config.data_schema)
        return code

    def samples(self, n=10):
        ret = []
        for i, row in enumerate(self):
            if i >= n:
                break
            ret.append(row)
        return ret

    def __iter__(self):
        """
        Iterate through the collection.
        :return:
        """
        entry = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            self.collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(entry, 'r') as fd:
            for line in fd:
                line = line.strip()
                if len(line) > 0:
                    item = json.loads(line)
                    if self.model is None:
                        yield item
                    else:
                        yield self.model(**item)

    def to_list(self):
        """
        Read the collection as list instead of iterator
        :return:
        """
        return list(self)


class DatasetStorageManager:
    def __init__(self, store_base=None):
        if store_base is None or store_base == '':
            store_base = get_storage_base_folder()
        self.base = store_base

    def list_dataset_stores(self) -> StoreList:
        base_dir = self.base
        stores = []

        if os.path.exists(base_dir):

            for store_name in os.listdir(base_dir):
                store_dir = os.path.join(base_dir, store_name)

                if os.path.isdir(store_dir) and is_name_legit(store_name):
                    stores.append(store_name)

        return StoreList(stores=stores)

    def list_datasets(self) -> DatasetListingResults:
        base_dir = self.base
        datasets = []

        if os.path.exists(base_dir):
            for store_name in os.listdir(base_dir):
                store_dir = os.path.join(base_dir, store_name)

                if os.path.isdir(store_dir):
                    for dataset_name in os.listdir(store_dir):
                        dataset_dir = os.path.join(store_dir, dataset_name)
                        dataset_home_folder = DatasetHomeFolder(dataset_dir)
                        if dataset_home_folder.marker_exist():
                            readme = readfile_or_default(dataset_home_folder.readme())
                            datasets.append(DatasetInfoSnippet(
                                datastore=store_name,
                                dataset=dataset_name,
                                readme=readme
                            ))
        return DatasetListingResults(items=datasets)

    def list_datasets_in_store(self, store_name) -> DatasetListingResults:
        base_dir = self.base
        datasets = []

        store_dir = os.path.join(base_dir, store_name)
        if os.path.isdir(store_dir):
            for dataset_name in os.listdir(store_dir):
                dataset_dir = os.path.join(store_dir, dataset_name)
                dataset_home_folder = DatasetHomeFolder(dataset_dir)
                if dataset_home_folder.marker_exist():
                    readme = readfile_or_default(dataset_home_folder.readme())
                    datasets.append(DatasetInfoSnippet(
                        datastore=store_name,
                        dataset=dataset_name,
                        readme=readme
                    ))
        return DatasetListingResults(items=datasets)

    def get_dataset_dir(self, store_name, dataset_name):
        store_dir = os.path.join(self.base, store_name, dataset_name)
        return DatasetHomeFolder(store_dir)

    def get_dataset_meta(self, store_name, dataset_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        return json.loads(readfile_or_default(dataset_home_folder.meta()))

    def get_dataset_source_info(self, store_name, dataset_name) -> Optional[SourceInfo]:
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        source_json = readfile_or_default(dataset_home_folder.remote_source(), None)
        if source_json is not None:
            return SourceInfo(**json.loads(source_json))
        return None

    def get_dataset_file_path(self, store_name, dataset_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        return dataset_home_folder.datafile()

    def get_dataset_readme(self, store_name, dataset_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        return readfile_or_default(dataset_home_folder.readme())

    def get_sample(self, store_name, dataset_name, collection):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        if os.path.isfile(dataset_home_folder.sample_file(collection)):
            with open(dataset_home_folder.sample_file(collection)) as fd:
                return list(read_jsonl(fd))
        return []

    def get_usage_code(self, store_name, dataset_name, collection_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        return readfile_or_default(dataset_home_folder.code_example(collection_name))

    def dataset_exist(self, store_name, dataset_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        return dataset_home_folder.marker_exist()

    def delete_dataset(self, store_name, dataset_name):
        dataset_home_folder = self.get_dataset_dir(store_name, dataset_name)
        shutil.rmtree(dataset_home_folder.base)

    def import_file(self, file, store_name, dataset_name, source_url=None):

        if self.dataset_exist(store_name, dataset_name):
            raise ValueError(f'dataset already exists under the name {store_name}/{dataset_name}')

        dataset_folder = self.get_dataset_dir(store_name, dataset_name)
        os.makedirs(
            dataset_folder.base, exist_ok=True
        )
        shutil.copy2(file, dataset_folder.datafile())
        self.extract_sample_and_code_usage(dataset_folder.datafile(), dataset_folder)

        if source_url is not None:
            with open(dataset_folder.remote_source(), 'w') as out:
                info = SourceInfo(url=source_url)
                json.dump(info.model_dump(mode='json'), out)

        with open(dataset_folder.marker(), 'w') as out:
            out.write('1')

    def import_url(self, url, store_name, dataset_name):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = str(uuid.uuid4())
            temp_file_path = os.path.join(temp_dir, file_name)
            try:
                urllib.request.urlretrieve(url, temp_file_path)
            except HTTPError as e:
                server_err = try_parse_error(e)
                if server_err is not None:
                    if 'reason' in server_err:
                        warnings.warn(server_err.get('reason', ''))
                raise e
            self.import_file(temp_file_path, store_name, dataset_name, source_url=url)
        return self.get_dataset_file_path(store_name, dataset_name)

    @staticmethod
    def extract_sample_and_code_usage(data_file, dataset_folder):
        with read_file(data_file) as reader:
            meta_file_dest = dataset_folder.meta()
            with reader.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'r') as fd:
                with open(meta_file_dest, 'wb') as out:
                    out.write(fd.read())

            for coll_name in reader.collections():
                coll = reader.collection(coll_name)
                with open(dataset_folder.sample_file(coll_name), 'w') as out:
                    samples = coll.samples(n=10)
                    for item in samples:
                        out.write(f'{json.dumps(item)}\n')
                with open(dataset_folder.code_example(coll_name), 'w') as out:
                    code = coll.code_usage()
                    out.write(code)


# Standard IO operations

def create(fp: str) -> 'DatasetFileWriter':
    """
    Create a dataset file to write
    :param fp: path to the file
    :return:
    """
    return DatasetFileWriter(fp)


def read_file(fp: str) -> 'DatasetFileReader':
    """
    Read a dataset file
    :param fp: path to the file
    :return:
    """
    return DatasetFileReader(fp)


def read(name: str, store_base: Optional[str] = None) -> 'DatasetFileReader':
    """
    Read a managed dataset file by name.
    :param name: name of the dataset file to locate
    :param store_base: where is the base folder or app
    :return:
    """
    manager = DatasetStorageManager(store_base)
    store_name, dataset_name = parse_dataset_name(name)
    located = manager.get_dataset_file_path(store_name, dataset_name)
    if os.path.exists(located):
        return DatasetFileReader(located)
    else:
        raise FileNotFoundError()


def import_file(name, file, store_base=None, exist_ok=True):
    manager = DatasetStorageManager(store_base=store_base)
    store, dataset = parse_dataset_name(name)
    if manager.dataset_exist(store, dataset) and exist_ok:
        print(f'dataset {name} already exists')
        return
    manager.import_file(file, store, dataset)


def import_url(name, url, store_base=None, exist_ok=True):
    manager = DatasetStorageManager(store_base=store_base)
    store, dataset = parse_dataset_name(name)
    if manager.dataset_exist(store, dataset) and exist_ok:
        print(f'dataset {name} already exists')
        return
    manager.import_url(url, store, dataset)


def exists(name, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    store, dataset = parse_dataset_name(name)
    return manager.dataset_exist(store, dataset)


def delete_dataset(name, store_base=None):
    manager = DatasetStorageManager(store_base=store_base)
    store, dataset = parse_dataset_name(name)
    return manager.delete_dataset(store, dataset)
