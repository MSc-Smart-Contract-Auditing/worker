from src.smart_contracts.jmespath_queries import FUNCTION_QUERY, INVOCATION_QUERY
from src.models.ast import Contract, Function, FunctionNode
from typing import List
from jqpy import jq


class ASTHandler:

    def __init__(self, contract: Contract):
        self.contract = contract
        self.lookup = self.__prepare_functions(contract)

    def __fix_indentation(self, source_code):
        lines = source_code.split("\n")
        if not lines:
            return source_code

        # Find the first non-whitespace character in the first line to determine the initial indentation
        first_line_indent = len(lines[-1]) - len(lines[-1].lstrip())
        # Adjust all lines to reduce the indentation by the amount found in the first line
        adjusted_lines = []
        for line in lines:
            # If there is witespace in the line
            if len(line) != len(line.lstrip()):
                line = line[first_line_indent:]
            adjusted_lines.append(line)

        return "\n".join(adjusted_lines)

    def __extract_source_code(self, function_ast):
        start, length = map(int, function_ast["src"].split(":")[:2])
        body = self.contract.raw[start : start + length]
        return self.__fix_indentation(body)

    def __prepare_functions(self, contract: Contract):
        function_asts = jq(FUNCTION_QUERY, contract.ast)
        lookup = {}

        for function_ast in function_asts:
            invocations = jq(INVOCATION_QUERY, function_ast)
            function = Function(
                id=function_ast["id"],
                name=function_ast["name"],
                source=self.__extract_source_code(function_ast),
            )

            lookup[function_ast["id"]] = FunctionNode(
                node=function, invocations=invocations
            )

        return lookup

    def get_ids(self):
        return list(self.lookup.keys())


import json
from src.models.requests import WorkUnit

with open("src/smart_contracts/compilation_result.json", "r") as file:
    data = json.load(file)


data = WorkUnit(**data)
print(data.root.name)
ASTHandler(data.root)


for contract in data.dependencies:
    print(contract.name)
    ASTHandler(contract)
