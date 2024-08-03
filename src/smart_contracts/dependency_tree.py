import json
from typing import List
from src.models.ast import Contract
from src.smart_contracts.ast_handler import ASTHandler
from src.models.ast import FunctionNodeAbstract
from src.models.requests import WorkUnit


class DependencyTree:

    def __init__(self, data: WorkUnit, max_depth: int = 2):
        self.main_contract = ASTHandler.get_contract_alias(data.root)
        print(self.main_contract)
        self.lookup = {
            ASTHandler.get_contract_alias(contract): ASTHandler(contract)
            for contract in [data.root] + data.dependencies
        }
        self.max_depth = max_depth

    def __traverse(self, invocations, depth):
        if depth >= self.max_depth:
            return []

        ret = []
        for invocation in invocations:
            contract_name = invocation.contract
            function_name = invocation.name
            function_node: FunctionNodeAbstract = self.lookup[contract_name].get_node(
                function_name
            )
            ret.append(function_node.node.source)
            ret += self.__traverse(function_node.invocations, depth + 1)

        return ret

    def tree(self, function_name: str):
        function_node: FunctionNodeAbstract = self.lookup[self.main_contract].get_node(
            function_name
        )

        return {
            "main": function_node.node.source,
            "dependencies": self.__traverse(function_node.invocations, 0),
        }


with open("src/smart_contracts/compilation_result.json", "r") as file:
    data = json.load(file)

data = WorkUnit(**data)
dt = DependencyTree(data)

# print(dt.tree("dumm2"))
print(dt.tree("dummy"))
print(dt.tree("getBalance"))
print(dt.tree("setBalance"))
