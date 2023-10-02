import json
import os
import re
import warnings


def try_parse_error(e):
    try:
        json_str = e.read()
        return json.loads(json_str)
    except KeyboardInterrupt as e:
        raise e
    except SystemExit as e:
        raise e
    except Exception as e:
        warnings.warn(str(e))
        return None


def readfile_or_default(fp, default=''):
    if os.path.exists(fp):
        with open(fp) as fd:
            return fd.read()
    return default


def count_slashes(input_string):
    dot_count = 0
    for char in input_string:
        if char == '/':
            dot_count += 1
    return dot_count


def is_name_legit(input_string):
    return bool(re.match(r'^(?=[a-zA-Z])[a-zA-Z0-9_-]*$', input_string))


def parse_dataset_name(name: str):
    dot_count = count_slashes(name)
    if dot_count == 0:
        store_name, dataset_name = 'main', name
    elif dot_count == 1:
        store_name, dataset_name = name.split('/')
    else:
        raise ValueError('dataset name must be [store_name]/[dataset_name] or [dataset_name]')

    if not is_name_legit(store_name) or not is_name_legit(dataset_name):
        raise ValueError('dataset name and store name must startswith a-zA-Z, and contains only [a-zA-Z0-9_-]')

    return store_name, dataset_name


def read_jsonl(line_stream):
    for line in line_stream:
        try:
            yield json.loads(line)
        except json.decoder.JSONDecodeError:
            pass
