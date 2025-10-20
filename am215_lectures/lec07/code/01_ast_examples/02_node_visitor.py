import ast

class FunctionFinder(ast.NodeVisitor):
    """
    A NodeVisitor that walks the AST and collects the names of all
    function definitions it finds.
    """
    def __init__(self):
        self.function_names = []

    def visit_FunctionDef(self, node):
        """This method is called for every function definition node."""
        print(f"Found function: {node.name}")
        self.function_names.append(node.name)
        # The generic_visit call is important to continue walking the tree
        # in case there are nested functions.
        self.generic_visit(node)

# A sample Python script as a string
source_code = """
import os

def process_data(data):
    print("Processing...")
    return len(data)

class MyAnalyzer:
    def analyze(self):
        pass
"""

tree = ast.parse(source_code)
finder = FunctionFinder()
finder.visit(tree)

print(f"\nCollected function names: {finder.function_names}")
