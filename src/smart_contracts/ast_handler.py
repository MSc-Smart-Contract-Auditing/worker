import jmespath
import json

from src.smart_contracts.jmes import FUNCTION_QUERY, INVOCATION_QUERY
from src.models.ast import Contract, Function, FunctionSignature, FunctionNodeAbstract


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

    def __extract_invocations(self, function_ast):
        invocations = jmespath.search(INVOCATION_QUERY, function_ast)
        signatures = []
        for invocation in invocations:
            invocation["contract"] = invocation["contract"].split(" ")[-1]
            signatures.append(FunctionSignature(**invocation))

        return signatures

    def __prepare_functions(self, contract: Contract):
        functions = {}
        function_asts = jmespath.search(FUNCTION_QUERY, contract.ast)
        test = function_asts[1]
        with open("src/smart_contracts/func.json", "w") as file:
            json.dump(test, file, ensure_ascii=False, indent=4)

        for function_ast in function_asts[1:2]:
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

        return functions

    def get_source(self, function_name):
        return self.functions[function_name].node.source

    def get_node(self, function_name):
        return self.functions[function_name]

    def get_function_names(self):
        return list(self.functions.keys())


with open("src/smart_contracts/compilation_result.json", "r") as file:
    data = json.load(file)

root = Contract(**data["root"])
handler = ASTHandler(root)
