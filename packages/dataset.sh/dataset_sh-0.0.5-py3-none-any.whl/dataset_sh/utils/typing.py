from datetime import date, datetime, time, timedelta

from dataset_sh.typing.core import FieldType, PydanticFieldDefinition, ClassDefinition, \
    DatasetSchema


def create_optional_field_type(name) -> FieldType:
    return FieldType.typed(
        'typing.Optional',
        [
            FieldType.simple(name)
        ]
    )


def guess_data_type(v):
    if isinstance(v, int):
        return 'int'
    elif isinstance(v, float):
        return 'float'
    elif isinstance(v, bool):
        return 'bool'
    elif isinstance(v, str):
        return 'str'
    elif isinstance(v, list):
        return 'list'
    elif isinstance(v, dict):
        return 'dict'
    elif isinstance(v, tuple):
        return 'tuple'
    elif isinstance(v, set):
        return 'set'
    elif isinstance(v, date):
        return 'datetime.date'
    elif isinstance(v, datetime):
        return 'datetime.datetime'
    elif isinstance(v, time):
        return 'datetime.time'
    elif isinstance(v, timedelta):
        return 'datetime.timedelta'
    else:
        return 'typing.Any'


def json_list_to_pydantic_code(items, max_row=None):
    clz_name = 'Model'
    field_map = {}
    for i, row in enumerate(items):
        if max_row is not None and i > max_row:
            break
        for col_name, cell in row.items():
            cell_type = guess_data_type(cell)
            if col_name in field_map:
                if field_map[col_name] != cell_type:
                    cell_type = 'typing.Any'
            field_map[col_name] = cell_type
    return DatasetSchema(
        entry_point=clz_name,
        classes=[
            ClassDefinition(
                name=clz_name,
                fields=[
                    PydanticFieldDefinition(
                        name=k,
                        v=create_optional_field_type(v)
                    )
                    for k, v in
                    field_map.items()]
            )
        ]
    )
