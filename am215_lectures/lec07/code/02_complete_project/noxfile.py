import nox

# Define the default sessions to run when nox is called without arguments.
nox.options.sessions = ["lint", "typecheck", "test", "docs"]
PYTHON_VERSIONS = ["3.11"]


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run the linter and formatter checks."""
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session):
    """Run the type checker."""
    # Install the package itself and its dependencies, plus the type checker.
    session.install(".", "ty")
    session.run("ty", "check", ".")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run the test suite."""
    # Install the package in editable mode with test dependencies.
    session.install(".[test]")
    session.run("pytest")


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build the documentation."""
    # Install documentation dependencies.
    session.install(".", "sphinx", "sphinx_autodoc_typehints", "numpydoc")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/_build/html")
