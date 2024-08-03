from pydantic import BaseModel
from typing import List


class Contract(BaseModel):
    name: str
    ast: object
    raw: str


class FunctionSignature(BaseModel):
    contract: str
    name: str


class Function(FunctionSignature):
    source: str


class FunctionNodeAbstract(BaseModel):
    node: Function
    invocations: List[FunctionSignature]


class FunctionNode(BaseModel):
    node: Function
    children: List[Function]
