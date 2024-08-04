from src.smart_contracts.jmespath_queries import FUNCTION_QUERY, INVOCATION_QUERY
from src.models.ast import Contract, Function, FunctionNode
from jqpy import jq

from typing import List


class ASTHandler:

    @staticmethod
    def process_contract(contract: Contract) -> List[FunctionNode]:
        return ASTHandler.__prepare_functions(contract)

    @staticmethod
    def __fix_indentation(source_code: str) -> str:
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

    @staticmethod
    def __extract_source_code(function_ast: object, source: str) -> str:
        start, length = map(int, function_ast["src"].split(":")[:2])
        body = source[start : start + length]
        return ASTHandler.__fix_indentation(body)

    @staticmethod
    def __prepare_functions(contract: Contract) -> List[FunctionNode]:
        function_asts = jq(FUNCTION_QUERY, contract.ast)
        lookup = {}

        for function_ast in function_asts:
            invocations = jq(INVOCATION_QUERY, function_ast)
            function = Function(
                id=function_ast["id"],
                name=function_ast["name"],
                source=ASTHandler.__extract_source_code(function_ast, contract.raw),
            )

            lookup[function_ast["id"]] = FunctionNode(
                function=function, invocations=invocations
            )

        return lookup
