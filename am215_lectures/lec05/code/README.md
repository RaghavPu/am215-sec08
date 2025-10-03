# Lecture 5 Code: Python Packaging Demos

This directory contains code examples to accompany the lecture on Python packaging. The examples are structured to demonstrate the evolution from fragile, ad-hoc methods to a robust, modern packaging workflow.

## Directory Structure

-   `01_anti_pattern_sys_path/`: Demonstrates the fragile `sys.path.append` hack.
-   `02_anti_pattern_pythonpath/`: Demonstrates using the `PYTHONPATH` environment variable.
-   `03_basic_package/`: A minimal, correct package using `pyproject.toml` and a `src` layout.
-   `04_full_package/`: A feature-complete package demonstrating optional dependencies, entry points, Cython extensions, and data file inclusion.
-   `05_project_using_package/`: Demonstrates using the packaged library as a dependency in a separate downstream project.
-   `Dockerfile`: Defines a consistent container environment for running the demos.
-   `build.sh`: A script to build the main development Docker image.
-   `run.sh`: A script to start an interactive session inside the development container.

## How to Run the Demos

This directory uses a "Docker-out-of-Docker" approach to provide a comfortable development environment while still allowing us to build portable Linux wheels in a specialized `manylinux` container.

1.  **Build the Main Development Image**

    From this directory (`am215_lectures/lec05/code/`), execute the `build.sh` script. You only need to do this once.

    ```bash
    ./build.sh
    ```

2.  **Start the Development Environment**

    Once the image is built, run the `run.sh` script to start an interactive session:

    ```bash
    ./run.sh
    ```

    This will drop you into an interactive `bash` shell inside the main development container. This container has `docker` installed and has access to your host's Docker socket, allowing you to build and run other containers from within it.

3.  **Follow the Demo Steps**

    Navigate into each demo directory and follow the instructions in its `README.md` file.

    ```bash
    # Start with the first demo
    cd 01_anti_pattern_sys_path
    cat README.md
    # ...run commands from the README...

    # Move to the next demo
    cd ../02_anti_pattern_pythonpath
    cat README.md
    # ...and so on...
    ```

3.  **Exit**

    When you are finished, simply type `exit` to leave the container shell.
