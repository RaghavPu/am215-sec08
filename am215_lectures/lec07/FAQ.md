# Lecture 7 FAQ - Code Quality & Documentation

This document contains answers to common questions that may arise from the "Code Quality & Documentation" lecture. It is designed to supplement the lecture by providing deeper explanations and exploring advanced topics.

---

### Static Assurance: Linting, Formatting, and Type Checking

#### What's the real difference between a linter and a formatter?
This is a crucial distinction. While they both analyze source code, they have different goals:

-   A **Formatter** (like `ruff format` or `black`) is concerned with **style**. Its only job is to automatically rewrite your code to conform to a consistent set of stylistic rules (line length, quote style, spacing, etc.). It does not find bugs; it makes your code look clean and uniform.
-   A **Linter** (like `ruff check` or `flake8`) is concerned with **correctness and quality**. It analyzes your code for potential bugs, bad practices, and suspicious constructs (like unused variables, shadowing built-ins, or using mutable default arguments). It finds problems but may or may not be able to fix them automatically.

In short: a formatter makes your code *look* good; a linter helps make your code *be* good.

#### If `ruff` is so great, why did we learn about `black`, `flake8`, etc.?
Understanding the historical context is important for two reasons:
1.  **Appreciation:** `ruff` is a modern tool that was created to solve the real-world problem of "linter fatigue"—having to install, configure, and run a half-dozen different tools (`black`, `isort`, `flake8`, `pylint`, etc.) that were often slow and had conflicting rules. Understanding the old, complex workflow helps you appreciate the speed and simplicity of a unified tool like `ruff`.
2.  **Compatibility:** You will frequently encounter projects in the wild that still use the older toolchain. Recognizing `black` in a `pyproject.toml` or `flake8` in a CI file is an important practical skill. `ruff` was designed to be a drop-in replacement for these tools, so knowing what they do helps you understand `ruff`'s configuration and rule sets.

#### What do the `select` codes in the `ruff` config mean? How do I configure it?
`ruff` has hundreds of linting rules, each identified by a code (e.g., `F841` for "unused variable"). These rules are grouped into categories based on the original tool they come from. The `select` option in your `pyproject.toml` tells `ruff` which categories of rules to enable.

The codes in our lecture's configuration are a common starting point:
-   **`E`** and **`W`**: Rules from `pycodestyle` (style errors and warnings, enforcing PEP 8).
-   **`F`**: Rules from `Pyflakes` (detects logical errors like unused imports or undefined names).
-   **`I`**: Rules from `isort` (enforces standard import order).
-   **`B`**: Rules from `flake8-bugbear` (finds likely bugs and design problems, like using mutable default arguments).

**How to configure `ruff`:**
1.  **Discover Rules:** The best way to learn about rules is on the official [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/).
2.  **Start Small:** The default `select` is a great starting point.
3.  **Gradually Add Rules:** As you become more familiar with `ruff`, you can add more rule categories to `select` or enable specific rules with `extend-select`. For example, you might add `"C90"` for cyclomatic complexity checks or `"T20"` for finding `print` statements.
4.  **Use `ruff rule`:** You can ask `ruff` to explain a rule directly from the command line:
    ```bash
    ruff rule F841
    ```
This command will print a detailed explanation of the rule and show non-compliant and compliant code examples.

#### Do type hints slow down my code?
**No.** This is a common and critical misconception. By default, the Python interpreter completely **ignores** type hints at runtime. They are treated as metadata that has no performance impact on your code's execution.

Type hints are only used by **static analysis tools**—separate programs like `ty` or `mypy` that you run outside of your main application. These tools read the hints to find potential errors before you even run the code.

There are some advanced libraries (like `pydantic` or `beartype`) that *can* check types at runtime, but this is an explicit, opt-in behavior that you have to specifically add to your code. Standard type hints have zero runtime cost.

#### How do I configure `ty` for strict checking?
The `ty` type checker does not have a single `strict = true` flag like `mypy`. Instead, it is designed to be strict by default, and you can increase its strictness further by configuring how it handles warnings.

A common way to enforce the highest level of strictness is to treat all warnings as errors. You can configure this in your `pyproject.toml` under the `[tool.ty.terminal]` section:

```toml
[tool.ty.terminal]
# Fail the run if there are any warnings.
error-on-warning = true
```

This ensures that the type checker will fail in a CI environment if it finds any potential type issues, even those it would normally classify as just a warning. You can also configure individual rule severities under `[tool.ty.rules]` for more fine-grained control.

#### Why is using a mutable default argument (e.g., `def func(arg=[])`) so bad?
This is one of the most famous "gotchas" in Python. The default argument object is created **only once**, when the function is first defined, not each time the function is called.

This means that every call to the function that relies on the default will be sharing and modifying the *exact same list object*.

```python
def add_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list

# First call works as expected
list1 = add_to_list(1) # list1 is [1]

# The default list has been modified!
# The next call appends to the SAME list.
list2 = add_to_list(2) # list2 is [1, 2], not [2]
```
A linter will immediately flag this pattern. The correct, safe idiom is to use `None` as the default and create a new list inside the function:
```python
def add_to_list_safe(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

#### You said type hints are just suggestions. How are they actually enforced?
This is a critical point. The Python interpreter itself **does not care about type hints**. It executes the code without validating them. The following code will run without a `TypeError` from Python, even though it's "wrong":

```python
def greet(name: str) -> None:
    print(f"Hello, {name}")

greet(123) # Python runs this just fine, printing "Hello, 123"
```
Enforcement comes from **external tools** that you run as part of your development workflow:
1.  **Static Type Checkers (like `ty` or `mypy`):** These are the primary enforcement mechanism. You run `ty check .` as a separate step, and it analyzes your code *without running it* to find type inconsistencies. This is what we do in our CI pipeline.
2.  **Runtime Type Checkers (like `beartype` or `pydantic`):** These are more advanced libraries that you can use as decorators. They *do* check types while your code is running and will raise errors if the types are incorrect. This adds a performance overhead but can be useful for validating data at critical boundaries, like API inputs.

For this course, we focus on static checking as the standard practice.

---

### The Abstract Syntax Tree (AST)

#### Why did we learn about the AST? Will I ever actually use this?
For most developers, the answer is no, you won't write `NodeTransformer`s every day. However, understanding the concept of the AST is incredibly valuable because it **demystifies static analysis**.

It shows you that tools like `ruff` are not magic. They work by following a clear, logical process: they parse your code into a tree structure, walk that tree, and apply rules at each node. Knowing this helps you:
1.  **Understand Linter Rules:** When a linter gives you a complex error, understanding that it's analyzing the code's structure can help you figure out what it's complaining about.
2.  **Appreciate Auto-Fixes:** You now know that `ruff check --fix` works by parsing your code, transforming the AST, and then "unparsing" it back into valid source code.
3.  **Unlock Advanced Capabilities:** If you ever need to do large-scale, programmatic refactoring of a codebase, the `ast` module is the right tool for the job.

#### What's the difference between `ast.NodeVisitor` and `ast.NodeTransformer` again?
-   `ast.NodeVisitor` is for **reading**. You use it to walk the tree and collect information without changing anything. Its `visit_*` methods do not have a meaningful return value.
-   `ast.NodeTransformer` is for **writing**. You use it to modify the tree. Its `visit_*` methods can return a new node, which will replace the original node in the tree. If you return `None`, the node is deleted.

Think of it this way: a `NodeVisitor` is like a building inspector who takes notes, while a `NodeTransformer` is like a renovation crew that can add, remove, or replace walls.

---

### Documentation: Docstrings & Sphinx

#### What's the difference between NumPy, Google, and reST docstring styles?
They are three different conventions for formatting the sections inside a docstring.
-   **reST (reStructuredText):** The native Sphinx format. It's very powerful but also very verbose, using explicit directives like `:param name: description`.
-   **NumPy Style:** The standard in the scientific Python community. It uses simple underlined headers (`Parameters\n----------`). It's clean and highly readable.
-   **Google Style:** Similar to NumPy style, but uses simple section headers without underlining (`Args:`).

The **`napoleon`** extension for Sphinx is the magic piece that allows Sphinx to understand the much more readable NumPy and Google styles and convert them into the reST that Sphinx expects. For scientific projects, **NumPy style is the recommended choice.**

#### Why use doctests if `pytest` is so much more powerful?
They serve different, complementary purposes:
-   **Doctests** are primarily for verifying that your **documentation is correct**. They are perfect for simple, pure functions where a minimal example clearly illustrates the function's main purpose. They ensure your examples never go out of date.
-   **`pytest`** is for robustly testing your **code's logic**. It is designed to handle complexity: edge cases, I/O, randomness, side effects, and complex state setup using fixtures.

**Rule of thumb:** If an example is simple enough to be in your docstring, it should probably be a doctest. Anything more complex belongs in your `tests/` directory and should be tested with `pytest`.

---

### Automation & Integration

#### Why is using CI better than forcing everyone to use Git pre-commit hooks?
While pre-commit hooks seem like a good idea for instant feedback, they are a poor choice for *enforcement* in a team setting. CI is the superior solution for several reasons:
1.  **Hooks are Local:** The `.git/hooks` directory is not version-controlled. Each developer must manually install and manage their own hooks. There is no guarantee everyone has them or that they are up-to-date.
2.  **Hooks Can Be Bypassed:** Any hook can be easily skipped with `git commit --no-verify`. This makes them an unreliable enforcement mechanism.
3.  **CI is Centralized and Authoritative:** The CI workflow is defined in a version-controlled file (e.g., `.github/workflows/ci.yml`). The rules are the same for everyone, and they run in a consistent, clean environment. When combined with branch protection rules, the CI pipeline becomes a non-bypassable quality gate.

Use local checks for **developer convenience**. Use CI for **project-wide enforcement**.

#### `make` vs. `nox` vs. `just`: Which task runner should I use?
-   **`make`**: The classic. It's language-agnostic and installed on nearly every Linux and macOS system. It's a great choice if your project involves many non-Python steps (e.g., compiling C code, running shell scripts). Its syntax can be quirky (e.g., requiring tabs).
-   **`nox`**: The Python-native choice. Its killer feature is creating isolated temporary environments for each task. This guarantees that your checks run in a clean, reproducible state, just like in CI. The configuration is a Python file, which is very flexible. This is the **recommended choice for most Python projects**.
-   **`just`**: A modern replacement for `make`. It has a simpler, cleaner syntax and avoids `make`'s quirks. It's excellent for running sequences of commands but doesn't have `nox`'s built-in environment management.

**Recommendation:** Start with `nox` for Python projects. If your needs are simpler or involve many other languages, `just` is a great modern alternative to `make`.

#### Why aren't tools like `ruff` and `ty` in `pyproject.toml`'s dependencies?
This is a key concept in packaging. The `[project.dependencies]` section is for packages that are required to *run* your code after it's installed. A user who installs your package needs `numpy` to run `compute_mean_std`, but they do not need `ruff` or `ty`.

Tools used for development—like linters, formatters, and test runners—are considered **development dependencies**. They are not required by the end-user. Including them in the main dependencies would needlessly bloat the installation for users.

These tools are managed in other ways:
1.  **Optional Dependencies:** They can be placed in `[project.optional-dependencies]`, like the `test` and `dev` groups in our example project. This allows a developer to install them explicitly with `pip install .[dev]`.
2.  **Direct Installation by CI/Task Runners:** As seen in our `noxfile.py` and `.github/workflows/ci.yml`, the tools are often installed directly by the automation script into a temporary environment. This is a very common and robust pattern as it isolates the tools from the project's runtime environment.

---

### Advanced Type Hinting

#### How does `typing.Protocol` work and why is it better than an ABC for type hints?
A `typing.Protocol` allows you to define an interface based on **behavior (duck typing)** rather than inheritance. This is a powerful concept for type hinting in flexible, modern Python code.

-   An **Abstract Base Class (ABC)** requires a class to explicitly inherit from it to be considered a valid subtype. This creates a rigid, nominal relationship.
-   A **`Protocol`** defines a set of methods and attributes that a class *should* have. Any class that has this structure is considered compatible by a static type checker, regardless of its inheritance tree.

Consider the `TrainableModel` example from the lecture. Any object, from any library, will be considered a valid `TrainableModel` by the type checker as long as it has a `.fit()` and `.predict()` method with the correct signatures. The object's author doesn't need to know about your protocol. This makes `Protocol` ideal for writing code that interoperates with objects from different libraries (e.g., `scikit-learn`, `statsmodels`, `xgboost`) that share a common API but not a common base class.

#### What is type inference and can I rely on it?
**Type inference** is the process by which a static type checker (like `ty` or `mypy`) deduces the type of a variable even when you haven't explicitly annotated it.

For example:
```python
x = 5          # The checker infers x is an `int`
y = [1, 2, 3]  # The checker infers y is a `list[int]`

def add_one(val): # No type hint for `val`
    return val + 1
```
In the `add_one` function, the checker sees the `+ 1` operation and can infer that `val` is likely an `int` or `float` and that the function returns an `int` or `float`.

However, you **should not rely on it for function signatures**. The primary purpose of type hints is to define the public contract of your functions. While inference is powerful for local variables inside a function, you should always explicitly annotate function parameters and return types. This serves as clear documentation and creates a stable API contract for other developers (and the type checker) to rely on.

#### How can type hints be used to generate tests?
This is an advanced and powerful technique, most commonly associated with **property-based testing** libraries like `hypothesis`.

When you write a test with `hypothesis`, you define *strategies* for generating test data. `hypothesis` is smart enough to use your type hints to infer these strategies automatically.

```python
from hypothesis import given
from hypothesis.strategies import lists, floats

# The "long way" - explicitly defining strategies
@given(xs=lists(floats()))
def test_mean_explicit(xs: list[float]):
    # ...

# The "magic" way - hypothesis infers the strategy from the type hint
@given
def test_mean_inferred(xs: list[float]):
    # ...
```
In `test_mean_inferred`, `hypothesis` sees the `xs: list[float]` annotation and automatically knows to generate lists of floating-point numbers as input. This tightens the link between your code's declared contract (the type hints) and its verification (the tests).

---

### Sphinx and Documentation Deep Dive

#### Can you explain the Sphinx workflow in more detail?
The four-step workflow can be broken down further:
1.  **`sphinx-quickstart`**: This is a one-time setup wizard. It creates the `docs/` directory and populates it with a `source/` subdirectory containing `conf.py` and `index.rst`. It asks you questions to generate a basic configuration.
2.  **`conf.py`**: This is the brain of your documentation. You edit this file to:
    -   Enable extensions in the `extensions = [...]` list. `autodoc` is essential for pulling in docstrings, and `napoleon` is essential for understanding NumPy-style formatting.
    -   Configure the look and feel, like the HTML theme.
3.  **`.rst` Files**: These are the content files for your documentation website. You use special Sphinx directives within them. The most important is `.. automodule:: my_package.main\n   :members:`. This tells `autodoc` to go to that Python module, inspect all its members (functions, classes), and insert their docstrings into the webpage at that location.
4.  **`sphinx-build`**: This is the final command. After first installing your package (e.g., `pip install -e .`), `sphinx-build` reads `conf.py`, processes all the `.rst` files, runs `autodoc` to pull in and render the docstrings, and then uses a "builder" (like the `html` builder) to write the final output files to a build directory.

#### How does Sphinx *actually* get the documentation from my code?
Sphinx's `autodoc` extension is not just parsing text files. It performs **live introspection** of your code. Here's how it works when it sees `.. automodule:: my_package.main`:

1.  **Import**: `autodoc` literally imports your module: `import my_package.main`. This is why your package must be installed (e.g., via `pip install -e .`), so that Sphinx can find and import it.
2.  **Inspect**: It then uses Python's built-in `inspect` module to look at the live objects inside the imported module (e.g., the `compute_mean_std` function object).
3.  **Extract**: It accesses the special attributes of these objects, primarily `__doc__` (the docstring), but also the function signature, default values, and type annotations.
4.  **Parse & Render**: If the `napoleon` extension is enabled, it takes the raw docstring text and parses the NumPy/Google style headers (`Parameters`, `Returns`, etc.) into the structured reST format that Sphinx understands.
5.  **Generate Output**: Finally, Sphinx takes this structured information and renders it into HTML, creating the clean, cross-linked documentation pages.

This is why your code must be importable for `autodoc` to work. If importing a file triggers code that has side effects or errors, the documentation build will fail.
