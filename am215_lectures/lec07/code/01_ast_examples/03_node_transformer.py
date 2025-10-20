import ast

class PowerToMultiply(ast.NodeTransformer):
    """
    A NodeTransformer that replaces the power operator (**)
    with the multiplication operator (*).
    """
    def visit_Pow(self, node):
        """This method is called for every Power operator node."""
        print("Found a `Pow` node, replacing it with `Mult`...")
        return ast.Mult()

# 1. Define the source code and parse it
source_code = "result = 2 ** 3"
tree = ast.parse(source_code)
print(f"Original AST: {ast.dump(tree)}")

# 2. Apply the transformation
transformer = PowerToMultiply()
new_tree = transformer.visit(tree)

# The new tree is functionally equivalent to "result = 2 * 3"
print(f"Modified AST: {ast.dump(new_tree)}")

# 3. Unparse the modified tree back into source code
new_code = ast.unparse(new_tree)
print(f"\nNew code: {new_code}")
