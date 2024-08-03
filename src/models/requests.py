from pydantic import BaseModel
from typing import List, Optional, Dict
from src.models.ast import FunctionNode


class Progress(BaseModel):
    current: int
    total: int


class Status(BaseModel):
    status: str
    progress: Optional[Progress] = None
    done: bool = False
    result: Optional[str] = None


class WorkUnit(BaseModel):
    lookup: Dict[int, FunctionNode]
    mainIds: List[int]


class Request(BaseModel):
    socket: str
    work: WorkUnit
