FUNCTION_QUERY = '.nodes[] | select(.nodeType == "ContractDefinition") | .nodes[] | select(.nodeType == "FunctionDefinition")'

INVOCATION_QUERY = '.. | select(type == "object" and .nodeType == "MemberAccess").referencedDeclaration'
