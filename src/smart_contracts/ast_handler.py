import jmespath

from src.smart_contracts.jmes import FUNCTION_QUERY, INVOCATION_QUERY
from src.models.ast import Contract, Function, FunctionSignature, FunctionNodeAbstract
from typing import List


class ASTHandler:
    def __init__(self, contract: Contract):
        self.contract = contract
        self.alias = contract.name.split("/")[-1].split(".")[0]
        self.functions = self.__prepare_functions(contract)

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

    def __extract_invocations(self, function_ast) -> List[FunctionSignature]:
        invocations = jmespath.search(INVOCATION_QUERY, function_ast)
        signatures: List[FunctionSignature] = []

        for invocation in invocations:
            if not (
                invocation["contract"] and invocation["contract"].startswith("contract")
            ):
                continue

            invocation["contract"] = invocation["contract"].split(" ")[-1]
            signatures.append(FunctionSignature(**invocation))

        return signatures

    def __prepare_functions(self, contract: Contract):
        functions = {}
        function_asts = jmespath.search(FUNCTION_QUERY, contract.ast)

        for function_ast in function_asts:
            function = Function(
                **{
                    "contract": self.alias,
                    "name": function_ast["name"],
                    "source": self.__extract_source_code(function_ast),
                }
            )
            invocations = self.__extract_invocations(function_ast)
            functions[function.name] = FunctionNodeAbstract(
                node=function, invocations=invocations
            )

        print(functions)
        return functions

    def get_source(self, function_name):
        return self.functions[function_name].node.source

    def get_node(self, function_name):
        return self.functions[function_name]

    def get_function_names(self):
        return list(self.functions.keys())
