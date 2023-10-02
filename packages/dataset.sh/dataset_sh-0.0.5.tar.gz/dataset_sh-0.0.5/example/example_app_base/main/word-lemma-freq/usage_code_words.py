import datetime
import typing
from enum import Enum, IntEnum
from pydantic import BaseModel

class WordCount(BaseModel):
    word : str
    freq : float