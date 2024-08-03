from pydantic import BaseModel
from typing import List, Optional
from src.models.ast import Contract


class WorkUnit(BaseModel):
    root: Contract
    dependencies: List[Contract]


class ProcessRequest(BaseModel):
    socket: str
    work: WorkUnit


class Progress(BaseModel):
    current: int
    total: int


class Status(BaseModel):
    status: str
    progress: Optional[Progress] = None
    done: bool = False
    result: Optional[str] = None
