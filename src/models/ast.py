from pydantic import BaseModel
from typing import List


class Contract(BaseModel):
    name: str
    ast: object
    raw: str


class Function(BaseModel):
    id: int
    name: str
    source: str


class FunctionNode(BaseModel):
    function: Function
    invocations: List[int]
