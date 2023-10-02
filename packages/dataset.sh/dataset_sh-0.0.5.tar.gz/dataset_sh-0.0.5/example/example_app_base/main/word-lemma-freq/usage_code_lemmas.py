import datetime
import typing
from enum import Enum, IntEnum
from pydantic import BaseModel

class LemmaCount(BaseModel):
    lemma : str
    freq : float