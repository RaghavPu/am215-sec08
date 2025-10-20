# Lecture 7 Code Examples: Abstract Syntax Trees (AST)

This directory contains simple, standalone scripts that demonstrate the core concepts of Python's `ast` module.

## What is the `ast` Module?

The `ast` module allows you to interact with Python source code as a tree structure. This is the foundation of all static analysis tools, including linters and formatters.

## How to Use These Examples

Run each script from your terminal to see its output.

### 1. `01_ast_dump.py`

This script shows how to parse a line of Python code into an AST and then print a detailed, developer-friendly representation of that tree.

```bash
python lec07/code/01_ast_examples/01_ast_dump.py
```

### 2. `02_node_visitor.py`

This script demonstrates how to "walk" or traverse an AST to find information without modifying it. The `FunctionFinder` class visits every function definition node and collects its name.

```bash
python lec07/code/01_ast_examples/02_node_visitor.py
```

### 3. `03_node_transformer.py`

This script shows how to programmatically modify code. The `PowerToMultiply` transformer finds all power operators (`**`) in the code and replaces them with multiplication operators (`*`). It then "unparses" the modified tree back into valid Python source code.

```bash
python lec07/code/01_ast_examples/03_node_transformer.py
```
