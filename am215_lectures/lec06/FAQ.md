# Lecture 6 FAQ - Testing and Automation

This document contains answers to common questions that may arise from the "Testing and Automation" lecture. It is designed to supplement the lecture by providing deeper explanations and exploring advanced topics.

---

### `pytest` Fundamentals

#### Why use `pytest` instead of the built-in `unittest` module?
While `unittest` is built into Python and is perfectly functional, `pytest` has become the de facto community standard for several key reasons that make testing easier and more powerful:
-   **Simplicity and Readability:** `pytest` uses the standard Python `assert` statement. This is easy to remember and makes tests clean and readable. `unittest` requires you to use a family of specific assertion methods like `self.assertEqual()`, `self.assertTrue()`, etc., which adds mental overhead.
-   **Less Boilerplate:** To write tests in `pytest`, you just need to create functions named `test_*` in a `test_*.py` file. `unittest` requires you to create a class that inherits from `unittest.TestCase` and then define your tests as methods of that class, which is more verbose.
-   **Powerful Fixtures:** `pytest`'s fixture system is a more powerful and flexible way to manage test state (like loading data or setting up complex objects) than the `setUp`/`tearDown` methods in `unittest`. Fixtures are reusable, explicit, and can be scoped to run only once per session, module, or class, making tests faster.
-   **Rich Plugin Ecosystem:** `pytest` has a massive ecosystem of plugins that add valuable functionality, such as `pytest-cov` for coverage, `pytest-benchmark` for performance testing, and `pytest-xdist` for running tests in parallel.

#### How does `pytest` know which files and functions are tests?
`pytest` uses a simple discovery mechanism based on naming conventions. When you run the `pytest` command, it scans your project directory and automatically finds tests that follow these rules:
1.  **File Names:** Test files must be named `test_*.py` or `*_test.py`.
2.  **Function Names:** Inside those files, functions that should be run as tests must be named `test_*`.
3.  **Class Names:** If you choose to group tests inside a class (which is optional), the class name must start with `Test`, and it cannot have an `__init__` method.

This "convention over configuration" approach means you don't have to manually register your tests. As long as you follow the naming scheme, `pytest` will find and run them.

#### What's the difference between a unit test and an integration test?
The difference lies in the scope of what is being tested.
-   A **Unit Test** focuses on a small, isolated piece of code (a "unit"), typically a single function or method. The goal is to verify that this one component works correctly on its own, without external dependencies like networks, databases, or other complex parts of your system. They should be fast and precise. For example, testing that `Vector.__add__` correctly sums two vectors is a unit test.
-   An **Integration Test** verifies that multiple components of your application work together correctly as a system. These tests are broader and check the interactions between modules. For example, a test that runs a full simulation pipeline—loading data from a file, executing the model, and saving a result plot—is an integration test.

A healthy project has a "testing pyramid": a large base of fast unit tests to verify individual components, a smaller layer of integration tests to ensure the pieces connect properly, and perhaps a few end-to-end tests at the very top.

#### `pytest.ini` vs `pyproject.toml` for configuration? Which should I use?
Both files can be used to configure `pytest`, but the modern best practice is to use **`pyproject.toml`**.

As we saw in Lecture 5, `pyproject.toml` is the standard file for configuring all aspects of a Python project, from build system dependencies to tool settings. Placing your `pytest` configuration under the `[tool.pytest.ini_options]` table in `pyproject.toml` keeps all your project's configuration in a single, predictable location. This reduces clutter in your project's root directory and makes it easier for other developers (and you!) to find and manage settings.

While `pytest.ini` is still fully supported, it's generally better to consolidate configuration into `pyproject.toml` for new projects.

#### What do the options in our `pytest` config mean? What are some other useful flags?
Configuring `pytest` in `pyproject.toml` ensures that tests are always run with the same consistent settings. Let's break down the configuration from the demo:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --cov=card_games"
```
-   **`testpaths = ["tests"]`**: This tells `pytest` to *only* look for tests in the `tests/` directory. For large projects, this can speed up test discovery and prevent `pytest` from accidentally picking up other files.
-   **`addopts = "-ra --cov=card_games"`**: This adds default command-line options to every `pytest` run.
    -   **`-ra`**: This flag provides a detailed **r**eport in the summary section for **a**ll test outcomes (passed, failed, skipped, etc.). Without it, `pytest` is very quiet about passed tests. This is useful for seeing exactly what ran.
    -   **`--cov=card_games`**: This option, from the `pytest-cov` plugin, enables coverage reporting and specifies that we want to measure coverage for the `card_games` package.

Here are some other common and very useful `pytest` flags to use from the command line:

-   **`-k <expression>`**: Run only tests whose names match the given string expression. For example, `pytest -k "addition or magnitude"` would run `test_vector_addition` and `test_vector_magnitude`. This is invaluable for focusing on a specific subset of tests.
-   **`-v`**: Verbose mode. It prints one test per line with its status ("PASSED", "FAILED") for a more detailed live view.
-   **`-x` or `--exitfirst`**: Stop the test session instantly on the first failing test. This is great for debugging, as it prevents you from being overwhelmed by a cascade of failures.
-   **`--lf` or `--last-failed`**: Only run the tests that failed during the last `pytest` run. This is arguably the most useful flag for rapid debugging cycles: run all tests, see what fails, fix, then run `pytest --lf` to quickly verify your fix.
-   **`--ff` or `--failed-first`**: Run all tests, but run the tests that failed last time *first*. This gives you the fastest possible feedback on your fixes while still ensuring the full test suite passes.

---

### Advanced Testing Techniques

#### How do I test code with floating-point numbers? Why can't I just use `assert result == 0.3`?
You should never use `==` to compare floating-point numbers because of how they are represented in binary. Most decimal fractions cannot be stored perfectly, leading to tiny precision errors. For example, `0.1 + 0.2` evaluates to `0.30000000000000004`, so a direct comparison to `0.3` will fail.

The correct approach is to check if the numbers are "close enough" within an acceptable tolerance. `pytest` and `numpy` provide excellent tools for this:
-   For single numbers (scalars), use `pytest.approx()`: `assert (0.1 + 0.2) == pytest.approx(0.3)`. It handles relative and absolute tolerances intelligently.
-   For NumPy arrays, use `numpy.testing.assert_allclose(array1, array2)`. This function is strongly preferred over `assert np.allclose(...)` because if the arrays do not match, it provides a much more detailed and helpful error message, showing you exactly which elements differ and by how much.

#### What is a "golden file" and when should I use one?
A "golden file" is a saved, trusted output from your model or analysis that you commit to your repository. It's used for **regression testing**, a technique to ensure that your model's output doesn't change unexpectedly as you refactor or modify your code.

This is especially useful when the "correct" output is too complex to calculate by hand, but you need to ensure it remains stable. The workflow is:
1.  Run your complex model once and save its output (e.g., a `.npy` file, a CSV, or even an image) to a dedicated directory like `tests/golden_files/`.
2.  Manually review this output to confirm it is correct. This becomes your "golden" standard.
3.  Write a test that runs the model and compares its new output to the golden file. For numerical data, this comparison should use a function like `np.testing.assert_allclose`. For other file types, you might compare file hashes.

If a future code change causes this test to fail, it signals an unintended "regression" in your model's behavior that you need to investigate.

#### What is a fixture? Why is it better than just calling a setup function in each test?
A **fixture** is a function that provides a fixed baseline state or data for your tests. You mark a function as a fixture with `@pytest.fixture`, and then any test that lists that function's name as an argument will receive its return value.

Fixtures are superior to manually calling setup functions for several reasons:
1.  **Caching and Efficiency:** `pytest` can cache the result of a fixture. If multiple tests use the same fixture, `pytest` can be configured to run it only once (e.g., once per test session), avoiding redundant and slow setup operations like loading a large file from disk for every single test.
2.  **Explicitness and Readability:** A test function's signature explicitly declares the dependencies it needs to run. This makes tests easier to understand.
3.  **Reusability and Modularity:** Fixtures can be defined in a central `conftest.py` file and used across your entire test suite. They can even use other fixtures, allowing you to build up complex test states from simple, modular components.

#### How can I test a stochastic function that gives a different result every time?
The key is to make the function deterministic *for the duration of the test*. As we saw in Lecture 3, this is achieved by controlling the source of randomness. Instead of relying on a global random state (`np.random.seed()`), your function should accept a seeded random number generator (RNG) object as an argument (`rng = np.random.default_rng(seed)`).

In a test, you can then create an RNG with a fixed seed and pass it to your function. Because the seed is the same, the sequence of "random" numbers will be identical every time the test runs, making the function's output reproducible and therefore testable.

To avoid re-declaring the RNG in every test, you can provide it with a fixture. This is an excellent pattern, but it must be done carefully to ensure test isolation. Because RNGs are stateful, you must ensure each test gets its own freshly-seeded instance. The default `function` scope of a fixture does this automatically.

```python
# in tests/conftest.py or your test file
import pytest
import numpy as np

@pytest.fixture
def seeded_rng():
    """A fixture that provides a freshly seeded RNG for each test."""
    # The fixture is re-run for each test, so each test gets its
    # own isolated, identically-seeded generator.
    return np.random.default_rng(42)

# in tests/test_my_stochastic_model.py
def test_simulation_a(seeded_rng):
    # This test gets a clean RNG seeded with 42
    result = run_simulation(rng=seeded_rng)
    assert result == pytest.approx(0.498)

def test_simulation_b(seeded_rng):
    # This test ALSO gets a clean RNG seeded with 42.
    # Its result is not affected by test_simulation_a having run.
    result = run_other_simulation(rng=seeded_rng)
    assert result == pytest.approx(0.501)
```

Using a wider scope like `@pytest.fixture(scope="session")` would be an anti-pattern here, as it would cause all tests to share the same stateful generator, leading to unpredictable results.

#### What is property-based testing and how is it different from parameterization?
Both are ways to test a function with multiple inputs, but they represent different philosophies.
-   **Parameterization** (`@pytest.mark.parametrize`) is example-based. You provide a specific, finite list of inputs and their expected outputs. You are telling the test, "for this exact input, I expect this exact output."
-   **Property-Based Testing** (using a library like `hypothesis`) is rule-based. Instead of specifying exact examples, you define a general rule or *property* that should be true for *any* valid input. The library then generates hundreds of diverse and complex inputs to try to find a counterexample that breaks your rule. For example, a property might be "for any list `x`, `sorted(x)` has the same length as `x`."

Property-based testing is excellent for finding weird edge cases that you might not have thought of yourself.

#### What is "mocking" and when should I use it?
Mocking is a technique used in unit testing to replace a real component that your code depends on with a "fake" or "mock" object that you control. You should use mocking when your code has external dependencies that are slow, unreliable, or complex, such as:
- A network call to a web API.
- A query to a large database.
- A function that performs a very long and complex calculation.

By replacing the real dependency with a mock, you can make your tests faster, more reliable (e.g., they can run without an internet connection), and you can easily simulate specific scenarios, like an API returning an error, to verify that your code handles them correctly. The `pytest-mock` plugin provides an easy-to-use `mocker` fixture for this.

#### How can I test for performance regressions?
The `pytest-benchmark` plugin is the standard tool for this. It provides a `benchmark` fixture that runs a given function many times to get a statistically reliable measurement of its execution time. The workflow is:
1. Write a test that uses the `benchmark` fixture to time your function.
2. Run `pytest --benchmark-save=<baseline_name>` to establish and save the current performance baseline.
3. After making code changes, run `pytest --benchmark-compare=<baseline_name>`. The plugin will automatically compare the new timings against the baseline and report any statistically significant performance regressions. This turns performance from a subjective concern into a testable requirement.

#### What does code coverage really tell me? Is 100% coverage the goal?
Code coverage is a metric that tells you which lines of your source code were executed by your test suite. It's a useful tool for identifying parts of your codebase that are **not tested at all**.

However, it is **not** a measure of test quality. 100% coverage is often a misleading and counterproductive goal. A test could execute a line of code but have no `assert` statement to actually verify that the code behaved correctly. Such a test would contribute to coverage but would be useless for catching bugs.

Think of coverage as a guide, not a goal. Use it to find untested code, but focus your effort on writing meaningful tests that verify your code's correctness, rather than just chasing a high coverage percentage.

---

### Continuous Integration with GitHub Actions

#### What are CI/CD, GitHub Actions, and "runners"?
-   **CI/CD** stands for Continuous Integration and Continuous Delivery/Deployment.
    -   **CI** is the practice of automatically building and testing your code every time a change is pushed to the repository. This helps catch bugs early.
    -   **CD** is the practice of automatically deploying your code (e.g., publishing a package to PyPI) after it successfully passes the CI tests.
-   **GitHub Actions** is a CI/CD platform built into GitHub. It lets you define automated workflows in response to events like `git push` or a pull request.
-   A **Runner** is the virtual machine (e.g., running Ubuntu, Windows, or macOS) that executes the jobs defined in your workflow. GitHub provides hosted runners, or you can set up your own for specialized needs (like GPU access).

#### What is a "matrix build" and why is it useful?
A matrix build is a feature in GitHub Actions that allows you to run the same job across multiple different configurations simultaneously. You define the different variables (like operating system and Python version) in a `matrix` strategy, and GitHub Actions automatically creates a job for every possible combination.

This is extremely valuable for scientific software because it allows you to easily verify **portability**. By testing your code on `ubuntu-latest`, `macos-latest`, and `windows-latest` with Python versions `3.9`, `3.10`, and `3.11`, you can be confident that your package will work correctly for users in different environments.

#### My tests pass locally but fail on GitHub Actions. Why?
This is a very common and important experience, as it's the primary problem that CI is designed to solve! It means there is a difference between your local environment and the clean environment of the CI runner. Common causes include:
1.  **Implicit Dependencies:** The CI runner starts as a clean slate. You might have a tool or library installed on your local machine that your code depends on, but you forgot to list it in your `pyproject.toml` or `requirements.txt`. The CI build fails because it's missing.
2.  **Operating System Differences:** Your code might rely on OS-specific behavior. For example, using backslashes in file paths (`data\\file.csv`) will work on Windows but fail on Linux. This is why matrix builds that test on multiple OSes are so valuable.
3.  **File Casing:** macOS and Windows filesystems are often case-insensitive by default, while Linux is case-sensitive. A statement like `import MyModule` might work locally if the file is named `mymodule.py`, but it will fail on a Linux runner.
4.  **Environment Variables:** The CI environment is not your local shell. It won't have your local `.bashrc` or environment variables set, unless you explicitly define them in the workflow file.

#### What does `uses: actions/checkout@v4` do?
This line in a workflow file tells GitHub Actions to use a pre-built, reusable piece of code called an "Action". The `actions/checkout` action is the official action for checking out your repository's code onto the CI runner. It essentially runs `git checkout` so that the subsequent steps in your job have access to your project's files.

The `@v4` part pins the action to a specific major version. This is a crucial best practice that ensures your workflow won't suddenly break if the action's author releases a new version with breaking changes.

#### How do I use secret keys, like a PyPI token, in a GitHub Actions workflow?
You should never hardcode sensitive information like API tokens directly in your workflow files. GitHub provides a secure way to handle this called **Secrets**.

The process is:
1.  Go to your repository's `Settings` > `Secrets and variables` > `Actions`.
2.  Create a new repository secret, giving it a name (e.g., `PYPI_API_TOKEN`) and pasting in the secret value.
3.  In your workflow YAML file, you can then access this secret using the `secrets` context: `${{ secrets.PYPI_API_TOKEN }}`.

GitHub ensures that secrets are encrypted and are never printed in the logs, so they remain secure.

#### What are branch protection rules and why are they important?
Branch protection rules are settings in GitHub that protect important branches (like `main`) from having broken or un-reviewed code merged into them. They are the enforcement mechanism that gives your CI pipeline its power.

By setting up a rule that **requires status checks to pass before merging**, you can configure GitHub to physically block the "Merge" button on a pull request if your CI workflow (e.g., the job that runs `pytest`) fails. This turns your automated test suite into a mandatory quality gate, ensuring that the `main` branch always remains in a stable, tested, and working state.

#### What are artifacts and how can they help me debug a failing CI run?
An **artifact** is a file or collection of files generated during a workflow run that you can save and download. This is incredibly useful for debugging CI failures where the text logs don't tell the whole story.

For example, if you have a test that generates a plot and then validates some property of it, and that test fails in the CI run, you can't see the incorrect plot. By adding a step that uses the `actions/upload-artifact` action (often conditionally, `if: failure()`), you can tell the workflow to upload the generated plot if the job fails. You can then download this artifact from the workflow summary page on GitHub to visually inspect what went wrong, which is much easier than trying to debug blind.
