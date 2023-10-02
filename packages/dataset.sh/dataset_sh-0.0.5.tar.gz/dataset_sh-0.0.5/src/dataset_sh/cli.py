#!/usr/bin/env python3

import json
from dataclasses import dataclass
from typing import Optional

import click

from dataset_sh.core import DatasetFileMeta
from dataset_sh.io import DatasetStorageManager, read_file
from dataset_sh.typing.codegen import CodeGenerator
from dataset_sh.utils.misc import parse_dataset_name


@dataclass
class AppCtx:
    base: Optional[str] = None


@click.group(name='dataset.sh')
@click.option('--base', '-b', envvar='DATASET_SH_STORAGE_BASE', help='location of base storage folder.',
              type=click.Path())
@click.pass_context
def cli(ctx, base):
    """Simple CLI tool with subcommands"""
    ctx.obj = DatasetStorageManager(store_base=base)


@click.command(name='print')
@click.argument('name')
@click.argument('action', type=click.Choice(['list-collections', 'readme', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection')
@click.pass_obj
def print_info(manager: DatasetStorageManager, name, action, collection):
    """
    print dataset information
    """
    store_name, dataset_name = parse_dataset_name(name)

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    if action == 'list-collections':
        meta = manager.get_dataset_meta(store_name, dataset_name)
        meta = DatasetFileMeta(**meta)

        click.echo(f'Total collections: {len(meta.collections)}')
        for coll in meta.collections:
            click.echo(coll.name)

    elif action == 'readme':
        readme = manager.get_dataset_readme(store_name, dataset_name)
        click.echo(readme)

    elif action == 'code':
        code = manager.get_usage_code(store_name, dataset_name, collection_name=collection)
        click.echo(code)

        meta = manager.get_dataset_meta(store_name, dataset_name)
        meta = DatasetFileMeta(**meta)
        coll = meta.find_collection(collection)

        if coll is not None:
            loader_code = CodeGenerator.generate_loader_code(
                store_name,
                dataset_name,
                collection,
                coll.data_schema.entry_point)
            click.echo('\n\n')
            click.echo(loader_code)

    elif action == 'sample':
        sample = manager.get_sample(store_name, dataset_name, collection)
        click.echo(json.dumps(sample, indent=2))


@click.command(name='inspect-file')
@click.argument('filepath', type=click.Path())
@click.argument('action', type=click.Choice(['list-collections', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection.')
@click.pass_obj
def inspect_file(manager: DatasetStorageManager, filepath, action, collection):
    """
    parse dataset file and print out information
    """

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    with read_file(filepath) as reader:
        if action == 'list-collections':
            collections = reader.collections()
            click.echo(f'Total collections: {len(collections)}')
            for coll in collections:
                click.echo(coll)

        elif action == 'code':
            coll = reader.collection(collection)
            code = coll.code_usage()
            schema = coll.config.data_schema
            loader_code = CodeGenerator.generate_file_loader_code(filepath, collection, schema.entry_point)
            click.echo(code)
            click.echo('\n\n')
            click.echo(loader_code)

        elif action == 'sample':
            sample = reader.collection(collection).samples()
            click.echo(json.dumps(sample, indent=2))


@click.command()
@click.argument('name')
@click.option('--force', '-f', default=False, help='Force remove dataset without confirmation.', is_flag=True)
@click.pass_obj
def remove(manager: DatasetStorageManager, name, force):
    """remove managed dataset"""
    store_name, dataset_name = parse_dataset_name(name)
    if not force:
        confirmation = click.prompt(f'Are you sure you want to remove dataset {name}? (y/N): ')
        if confirmation.lower() == 'y':
            manager.delete_dataset(store_name, dataset_name)
    else:
        manager.delete_dataset(store_name, dataset_name)


@click.command(name='list')
@click.option('--store', '-s', help='select dataset store space to list.')
@click.pass_obj
def list_datasets(manager: DatasetStorageManager, store):
    """list datasets"""
    items = []
    if store:
        items = manager.list_datasets_in_store(store).items
    else:
        items = manager.list_datasets().items

    click.echo(f'Found {len(items)} datasets:\n')
    items = sorted(items, key=lambda x: f'{x.datastore} / {x.dataset}')
    for item in items:
        click.echo(f'  {item.datastore}/{item.dataset}')


@click.command(name='import')
@click.argument('name')
@click.option('--url', '-u', help='url of the dataset file to import')
@click.option('--file', '-f', help='local file path of the dataset file to import', type=click.Path())
@click.pass_obj
def import_(manager, name, url, file):
    """import dataset from url or file"""
    if url is not None and file is not None:
        click.echo('Usage: import [NAME] -u [url]')
        click.echo('Usage: import [NAME] -f [file-path]')
        raise click.Abort()

    if url is None and file is None:
        click.echo('Usage: import [NAME] -u [url]')
        click.echo('Usage: import [NAME] -f [file-path]')
        raise click.Abort()

    store_name, dataset_name = parse_dataset_name(name)

    if url is not None:
        click.echo(f'importing remote file from {url}')
        manager.import_url(url, store_name, dataset_name)
    elif file is not None:
        click.echo(f'importing local file from {file}')
        manager.import_file(file, store_name, dataset_name)


# Add subcommands to the main command
cli.add_command(print_info)
cli.add_command(remove)
cli.add_command(list_datasets)
cli.add_command(inspect_file)
cli.add_command(import_)

if __name__ == '__main__':  # pragma: no cover
    cli()
