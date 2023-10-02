import datetime
import typing
from enum import Enum, IntEnum
from pydantic import BaseModel

class NumberSequence(BaseModel):
    oeisID : str
    description : str
    seq : typing.List[int]