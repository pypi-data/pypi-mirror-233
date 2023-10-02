import os
import json
import warnings

_CONFIG_FILE = '~/.dataset_sh_config.json'


def get_storage_base_folder():
    """
    Read storage base folder path with the following order:
    1. ENV: DATASET_APP_STORAGE_LOCATION
    2. Config File: '~/.dataset_sh_config.json'
    3. DEFAULT_VALUE: '~/dataset_sh/storage'
    :return: storage base folder location
    """
    v = os.environ.get('DATASET_APP_STORAGE_LOCATION', None)
    if v is None:
        cfg_path = os.path.expanduser(_CONFIG_FILE)
        if os.path.exists(cfg_path):
            with open(cfg_path) as fd:
                try:
                    cfg = json.load(fd)
                    if 'storage' in cfg:
                        if 'location' in cfg['storage']:
                            v = cfg['storage']['location']
                except json.decoder.JSONDecodeError:
                    warnings.warn('Cannot parse dataset local config file.')

    if v is None:
        v = '~/dataset_sh/storage'

    return os.path.expanduser(v)
