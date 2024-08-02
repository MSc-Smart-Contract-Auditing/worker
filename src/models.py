from pydantic import BaseModel
from typing import List


class Contract(BaseModel):
    name: str
    ast: object
    raw: str


class WorkUnit(BaseModel):
    root: Contract
    dependencies: List[Contract]


class ProcessRequest(BaseModel):
    socket: str
    work: WorkUnit
