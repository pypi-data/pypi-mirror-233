# Getting Started

`dataset.sh` is a dataset manager designed to simplify the process of installing, managing, and publishing datasets.
We hope to make working with datasets as straightforward as using package managers like npm or pip for programming
libraries.

## Motivation

To understand the need for `dataset.sh`, consider how programming libraries are distributed both with and without
package managers like npm, pip, and Maven:

| Feature          | Without Package Manager                                                                               | With Package Manager (npm, pip, Maven, etc.)                  |
|------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| Folder Structure | Often adopts various project/folder structures                                                        | Standardized project/folder structures                        |
| Installation     | Manual download, reading instructions, installing dependencies, configuring, building, and installing | Automated installation process managed by the package manager |
| Management       | You must manually track:<br/>- Installed libraries<br/>- Install locations<br/>- Installed versions   | Package managers keep track of everything                     |

The current state of dataset distribution resembles the older, manual methods of distributing programming libraries.
`dataset.sh` aims to offer an experience similar to modern package managers.

| Feature          | Without Dataset Manager                                                                               | With `dataset.sh`                                                                                                                          |
|------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Folder Structure | No standardized project structure                                                                     | Standardized project structure                                                                                                             |
| Installation     | Manual download, reading instructions, installing dependencies, configuring, building, and installing | Automated installation process managed by `dataset.sh`<br/>and `dataset.sh` will generate reader in python for each dataset automatically. |
| Management       | You must manually track:<br/>- Installed datasets<br/>- Install locations                             | `dataset.sh` keeps track of everything for you                                                                                             |

## Install

To get started, you can install `dataset.sh` via pip:

```bash
pip install dataset.sh
dataset.sh --help
```

## Data Model

The data model of `dataset.sh` closely resembles that of MongoDB.

A dataset file in dataset.sh can contain one or more collections. Each collection is identified by a collection name and
comprises a list of JSON objects that share the same schema.

Additionally, a dataset file may include a list of binary files. These can be referenced by items in any of the
collections.

## Read data

### Importing Datasets

#### Import a local file

```shell
dataset.sh import [NAME] -f [URL]
```

```python
import dataset_sh

dataset_sh.import_file('name-of-the-dataset', 'path-to=the-dataset-file')
```

#### Import from url

You can import a dataset using cli: (you can name the dataset)

```shell
dataset.sh import [NAME] -u [URL]
```

or in python

```python
import dataset_sh

dataset_sh.import_url('name-of-the-dataset', url='url-of-the-dataset')
```

### Read dataset content

```python
import dataset_sh

# Or you can also read from a file 
# with dataset_sh.read_file('./some-file.dataset') as reader: 
with dataset_sh.read('name-of-the-installed-dataset') as reader:
    print(reader.collections())  # list collections inside this dataset

    for item in reader.coll('coll_1'):
        print(item)  # iterative through items under coll_1
        break

    print(reader.binary_files())

    with reader.open_binary_file('name-of-binary-file') as bin_file:
        bin_file.read()
```

### Generate dataset related data structure

```shell
dataset.sh print [NAME] code
```
