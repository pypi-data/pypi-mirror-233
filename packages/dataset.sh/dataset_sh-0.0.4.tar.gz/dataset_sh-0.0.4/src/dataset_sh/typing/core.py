from typing import Union, Optional, List

from pydantic import BaseModel


class EnumEntry(BaseModel):
    name: str
    value: Union[int, str]


class FieldType(BaseModel):
    is_parametric: bool
    name: str
    children: Optional[List['FieldType']] = None

    @staticmethod
    def simple(name):
        return FieldType(is_parametric=False, name=name)

    @staticmethod
    def typed(name, children):
        return FieldType(is_parametric=True, name=name, children=children)


class PydanticFieldDefinition(BaseModel):
    name: str
    type: FieldType


class EnumDefinition(BaseModel):
    name: str
    enum_entries: Optional[List[EnumEntry]]

    def is_int(self):
        if self.enum_entries is not None and len(self.enum_entries) > 0:
            return isinstance(self.enum_entries[0].value, int)
        return False


class ClassDefinition(BaseModel):
    name: str
    fields: List[PydanticFieldDefinition]


class DatasetSchema(BaseModel):
    entry_point: str
    classes: List[Union[EnumDefinition, ClassDefinition]]
