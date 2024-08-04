def get_function_definitions(data):
    result = []
    for node in data["nodes"]:
        if node["nodeType"] == "ContractDefinition":
            for sub_node in node["nodes"]:
                if sub_node["nodeType"] == "FunctionDefinition":
                    result.append(sub_node)
    return result


def get_referenced_declarations(data):
    result = []

    def recursive_search(node):
        if isinstance(node, dict):
            if (
                node.get("nodeType") == "MemberAccess"
                and "referencedDeclaration" in node
            ):
                result.append(node["referencedDeclaration"])
            for value in node.values():
                recursive_search(value)
        elif isinstance(node, list):
            for item in node:
                recursive_search(item)

    recursive_search(data)
    return result
