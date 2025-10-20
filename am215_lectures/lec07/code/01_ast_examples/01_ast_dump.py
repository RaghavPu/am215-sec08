import ast

# A simple line of Python code
source_code = "x = (1 + 2) * 3"

# 1. Parse the code into an AST
tree = ast.parse(source_code)

# 2. Dump the tree to see its structure
# The indent parameter makes the output readable.
print(ast.dump(tree, indent=4))
