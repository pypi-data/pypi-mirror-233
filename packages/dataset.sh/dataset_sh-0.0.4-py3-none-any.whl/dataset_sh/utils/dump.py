from dataset_sh import create


def dump_single_collection(fn, name, data):
    with create(fn) as out:
        out.add_collection(name, data, data[0].__class__)


def dump_collections(fn, data_dict):
    with create(fn) as out:
        for name, data in data_dict.items():
            out.add_collection(name, data, data[0].__class__)
