FUNCTION_QUERY = "nodes[?nodeType == 'ContractDefinition'].nodes[] | [?nodeType == 'FunctionDefinition']"

# INVOCATION_QUERY = "expression[?nodeType == 'FunctionCall']"
INVOCATION_QUERY = """
body.statements[?expression.nodeType == 'FunctionCall'].expression.expression
.{contract: expression.typeDescriptions.typeString, name: memberName}
"""
