# Lecture 5 FAQ - Python Packaging

This document contains answers to common questions that may arise from the "Python Packaging" lecture. It is designed to supplement the lecture by providing deeper explanations and exploring advanced topics.

---

### Core Concepts & Project Structure

#### Why is the `src/` layout so important? Can I get away without it?
You *can* get away without it for simple projects, but the `src/` layout is a professional best practice that prevents a subtle and confusing class of errors.

The problem it solves is **import ambiguity**. Imagine you are in the root of your project, which does *not* have a `src/` layout. If you run `pytest` or open a Python shell and type `import card_games`, Python will find the local `card_games/` directory first and import it. Your tests might pass, and everything seems to work. However, you are testing the local source code, *not* the code that was actually installed by `pip`. If there was an error in your `pyproject.toml` that caused the installation to be incomplete, you would never know, but your users would get a broken package.

The `src/` layout solves this. By moving the package code into `src/`, the `card_games` package is no longer on the top-level path. When you are in the project root, `import card_games` will now fail unless you have correctly installed the package (e.g., with `pip install -e .`). This forces you to always test against the installed version, ensuring that what you test is what your users will get.

#### What's the real difference between `sys.path.append` and `PYTHONPATH`?
Both are "anti-patterns" for making a library importable because they create implicit, fragile dependencies on your local file system. However, they differ in scope:

-   **`sys.path.append(...)`**: This is temporary and local to a single script. It only affects the Python process that is currently running. As soon as the script finishes, the change to `sys.path` is gone.
-   **`export PYTHONPATH=...`**: This is an environment variable that affects your entire shell session. Any Python script you run from that shell will have this path added to its `sys.path`. This is arguably more dangerous because its effect is broader and more "hidden." A background script or an unrelated project could accidentally import code from a `PYTHONPATH` directory, leading to very confusing behavior.

Editable installs (`pip install -e .`) are the correct, modern solution to this problem for local development.

#### What should I put in `__init__.py`?
The `__init__.py` file has two main purposes:
1.  **To mark a directory as a Python package.** For this, the file can be completely empty.
2.  **To define the package's public API.** This is the more powerful use case. By importing key classes and functions from your submodules into `__init__.py`, you create a single, convenient entry point for your users.

For example, in our `card_games` package, importing `Deck` in `src/card_games/__init__.py` allows users to write `from card_games import Deck` instead of the more verbose `from card_games.deck import Deck`. This hides your internal file structure and creates a cleaner, more stable API.

It's also a common convention to expose the package's version in this file, especially when using a tool like `setuptools-scm`:
```python
# src/my_package/__init__.py
from .my_module import MyClass
from ._version import version as __version__
```

---

### `pyproject.toml` Deep Dive

#### What's the difference between a build tool and a build backend?
This separation is the core principle of modern Python packaging (PEP 517).

-   A **build tool** (or "frontend") is the user-facing command you run. Examples are `pip`, `build`, and `uv`. Its job is to read `pyproject.toml`, create an isolated build environment with the required build dependencies, and then call the build backend to do the actual work.
-   A **build backend** is the library that does the heavy lifting of creating the package artifacts. Examples are `setuptools`, `hatchling`, and `flit-core`. It's responsible for finding all the files, compiling any C/Cython code, and bundling everything into the final `sdist` and `wheel` files.

This separation is powerful because it allows you to use your favorite frontend (e.g., the fast `uv` tool) with any project, regardless of which backend the project's author chose.

#### When should I use `setuptools` vs. `flit` or `hatchling`?
-   **`setuptools`**: The battle-tested, powerful default. If your project has any complexity, especially compiled extensions (C/Cython/Fortran), `setuptools` is the safest and most feature-rich choice.
-   **`flit-core`**: A minimalist, fast backend designed for simple, pure-Python packages. If your project is just Python code with no complex build steps, `flit` is a great, simple option.
-   **`hatchling`**: A modern, extensible, and standards-compliant backend. It's part of the larger `hatch` toolchain, which aims to provide a unified solution for environment management, testing, and publishing. It's an excellent modern choice, especially for pure-Python projects.

**Recommendation:** Start with `setuptools`. It can handle anything you throw at it. If you later find your project is simple and you value speed or minimalism, you can easily switch to `flit` or `hatchling`.

#### What are version specifiers (`>=`, `~=`) and should I pin my dependencies (`==`)?
This is a critical distinction between packaging a **library** versus an **application**.

-   **For a library (in `pyproject.toml`):** You should use *loose* or "abstract" dependencies.
    -   `numpy>=1.21`: Requires at least version 1.21.
    -   `scipy~=1.8.0`: "Compatible release." This means `>=1.8.0` but `<1.9.0`. It's good for dependencies that use semantic versioning, as it allows bug fixes but prevents breaking changes.
    -   **Why?** Using loose pins prevents your library from causing dependency conflicts in downstream projects. If you require `numpy==1.21.0` and another library requires `numpy==1.22.0`, a user cannot install both.

-   **For an application (in `requirements.txt`):** You should use *strict* or "concrete" dependencies for reproducibility.
    -   `numpy==1.21.5`
    -   **Why?** For a final application, you want to lock down the entire environment to ensure it's perfectly reproducible, as we discussed in Lecture 3.

---

### Wheels, Compilation, and Data

#### What is an ABI and why does it matter for wheels?
**ABI** stands for **Application Binary Interface**. It's a low-level contract that defines how compiled code (like a C extension) interacts with the Python interpreter at the binary level. It specifies details like how function calls are structured, how data is laid out in memory, and how exceptions are handled.

This contract is not guaranteed to be stable across different Python versions. For example, the internal structure of a `PyObject` might change between Python 3.10 and 3.11. If this happens, a C extension compiled for Python 3.10 will crash when used with the Python 3.11 interpreter.

The ABI tag in a wheel's filename (e.g., `cp310` for CPython 3.10) is crucial because it tells `pip` which Python interpreter the wheel's compiled code is compatible with. This prevents `pip` from installing a wheel that would break at runtime.

#### How does `importlib.resources` actually find the data files?
Python's import system is backed by a system of **loaders**. A loader is an object that knows how to load a module from a specific source. For example, there's a loader for finding `.py` files on the file system and another for loading modules from inside a `.zip` archive.

When you install a package, it can be installed in different ways:
-   As loose files in `site-packages` (a standard wheel install).
-   As a single `.egg` or `.zip` file in `site-packages`.
-   As a link back to your source directory (an editable install).

The `importlib.resources` module provides a high-level, unified API that works with these loaders. When you call `files('card_games').joinpath('data.json')`, the loader for the `card_games` package figures out where it's located—whether on the filesystem or inside a zip file—and provides a way to access the `data.json` resource. This is why it's so robust; it abstracts away the details of the installation format.

#### Why use Cython instead of just writing C code?
Cython offers a much smoother "off-ramp" from pure Python to C-level performance.
1.  **Incremental Optimization:** You can start by renaming a `.py` file to `.pyx` and it will compile and run. Then, you can add static `cdef` type declarations *only* to the performance-critical parts of your code (like tight loops) to get massive speedups. This is much easier than rewriting an entire module in C.
2.  **Python-like Syntax:** Cython's syntax is a superset of Python's. You can continue to use familiar Python data structures and control flow, which is much simpler than writing raw C code using the Python C API.
3.  **Easy C Interoperability:** Cython makes it very easy to call external C/C++ libraries, acting as a powerful "glue" language.

For many scientific tasks, Cython provides the perfect balance between Python's ease of use and C's raw speed.

#### Why did my wheel upload get rejected with an "unsupported platform tag" error?
This is a common and important error. It means you built a wheel on your local Linux machine and tried to upload it to PyPI. The wheel likely has a platform tag like `linux_x86_64`.

PyPI rejects these because a wheel compiled on one Linux distribution (e.g., the latest Arch Linux) is not guaranteed to work on another (e.g., an older CentOS). This is due to differences in core system libraries like `glibc`. To solve this problem and ensure that wheels are truly portable across Linux distributions, the Python community created the **`manylinux` standard**.

A `manylinux` wheel is built inside a special Docker container that has a very old, stable version of `glibc` and other core libraries. When you build your wheel in this environment, any required newer libraries are bundled directly into the wheel itself. The resulting wheel gets a tag like `manylinux2014_x86_64`, which signals to `pip` and PyPI that it is highly portable.

The standard solution is to use the official `pypa/manylinux` Docker images to build your wheels for distribution. This is exactly what we do in the lecture demos, using a "Docker-out-of-Docker" pattern where our main development container launches a separate, minimal `manylinux` container just for the build step.

---

### Workflow & Professional Practices

#### How does `setuptools-scm` know the version if I'm not on a tag?
`setuptools-scm` is very clever about this. It runs `git describe --dirty --tags` under the hood to determine the version.
-   If you are on a tag like `v0.2.0`, the version is exactly `0.2.0`.
-   If you are 3 commits past that tag, it will generate a development version string like `0.2.0.post3.dev0+g<hash>`, where `<hash>` is the current commit hash. This follows PEP 440 and ensures every commit has a unique, identifiable version.
-   If you have uncommitted changes in your working directory, it will append `.dirty` to the version string, signaling that the code is not in a clean state.

This makes it an incredibly robust tool for ensuring that every build of your package has a version that is traceable back to a specific state in your `git` history.

#### Why is the MIT license so popular for scientific code?
The MIT license is a **permissive** license. It essentially says: "You can do whatever you want with this code (use it, modify it, sell it), as long as you include the original copyright and license notice in your copy of the software."

This is popular in science and academia for a few key reasons:
1.  **Maximizes Adoption:** It places almost no restrictions on users, encouraging the widest possible use of the software in both academic research and commercial products.
2.  **No "Viral" Effect:** Unlike "copyleft" licenses like the GPL, it does not require derivative works to also be open source. This makes companies much more comfortable using MIT-licensed code.
3.  **Simplicity:** It is short, easy to understand, and legally unambiguous.

For researchers who want their work to have the greatest possible impact and be used by the largest number of people, the MIT license is often the ideal choice.

#### If `uv` is so great, why did you show the `pip`/`build`/`twine` workflow?
It's important to understand the underlying components of the packaging ecosystem. `pip`, `build`, and `twine` are the foundational, separate tools that define the standard workflow.
-   `build` is the canonical tool for running a build backend.
-   `twine` is the canonical tool for securely uploading artifacts.
-   `pip` is the canonical installer.

`uv` is a fantastic, modern tool that provides a fast, integrated interface on top of these same standard protocols. By learning the components first, you understand *what* `uv` is doing under the hood. This knowledge is invaluable for debugging complex issues and for situations where you might be in an environment that only has the standard tools available. It's like learning to drive a manual transmission car before driving an automatic—you gain a deeper understanding of the mechanics, even if you end up using the more convenient option day-to-day.
