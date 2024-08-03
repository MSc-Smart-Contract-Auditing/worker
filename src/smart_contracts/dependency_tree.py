import json
from typing import List
from src.smart_contracts.ast_handler import ASTHandler
from src.models.ast import FunctionNode
from src.models.requests import WorkUnit


class DependencyTree:

    def __init__(self, data: WorkUnit, max_depth: int = 3):

        self.lookup = {
            key: value
            for contract in data.dependencies
            for key, value in ASTHandler.process_contract(contract).items()
        }

        main_contract_nodes = ASTHandler.process_contract(data.root)
        self.main_ids = main_contract_nodes.keys()
        self.lookup.update(main_contract_nodes)
        self.max_depth = max_depth

    def __traverse(self, invocations, depth):
        if depth >= self.max_depth:
            return []

        nodes: List[FunctionNode] = [
            self.lookup[invocation] for invocation in invocations
        ]

        # Breath first keeps most relevant code closer to the top
        ret = []
        for node in nodes:
            ret.append(node.function.source)
        for node in nodes:
            ret += self.__traverse(node.invocations, depth + 1)
        return ret

    def get_main_ids(self):
        return self.main_handler.get_ids()

    def tree(self, id: int):

        if id not in self.main_ids:
            return None  # TODO: Throw error

        function_node: FunctionNode = self.lookup[id]

        return {
            "main": function_node.function.source,
            "dependencies": self.__traverse(function_node.invocations, 0),
        }


with open("src/smart_contracts/compilation_result.json", "r") as file:
    data = json.load(file)

data = WorkUnit(**data)
dt = DependencyTree(data)


for item in dt.lookup.items():
    print(item)

print()
print()

result = dt.tree(46)
print(result["main"])
for dependency in result["dependencies"]:
    print(dependency)
