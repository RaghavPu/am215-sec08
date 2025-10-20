# Particle Diffusion Simulation

This module provides a simple object-oriented framework to simulate and visualize 2D particle diffusion. It is designed to demonstrate several key concepts from Lecture 4, including properties with setters, Abstract Base Classes (ABCs), inheritance, and metaprogramming for creating an extensible, plug-in-style architecture.

## Files

-   `__init__.py`: Marks the directory as a Python package.
-   `particle.py`: Contains the `Particle` class. This class demonstrates using a `@property` with a setter to provide an intuitive polar coordinate API (`r`, `theta`) on top of the underlying Cartesian storage (`x`, `y`).
-   `walkers.py`: Defines the `RandomWalker` Abstract Base Class, which establishes the "contract" for all walker types. It also contains concrete implementations (`StandardWalker`, `BiasedWalker`) and uses the `__init_subclass__` dunder method to create a self-registering system for walkers.
-   `run_simulation.py`: The main executable script. It sets up simulation parameters, selects a walker type from the registry by name, runs the main loop, and calls the animation function.
-   `animate.py`: Contains the `create_animation` function, which uses `matplotlib` to generate and save a GIF of the particle trajectories.
-   `requirements.txt`: Lists the Python dependencies (`matplotlib`, `Pillow`).
-   `Dockerfile`, `docker_build.sh`, `docker_run.sh`: Files for building and running the simulation inside a Docker container, ensuring a fully reproducible environment.

## How to Use

This simulation requires `matplotlib` and `Pillow`. It is recommended to use a virtual environment.

### 1. Running Directly

1.  **Create a virtual environment and install dependencies:**
    From the `am215_lectures/lec04/code/diffusion/` directory, run:
    ```bash
    # Create and activate a virtual environment
    uv venv
    source .venv/bin/activate

    # Install dependencies
    uv pip install -r requirements.txt
    ```

2.  **Run the simulation:**
    From the root directory of the repository, run the simulation script as a module:
    ```bash
    python -m am215_lectures.lec04.code.diffusion.run_simulation
    ```
    This will execute the main simulation loop and save the resulting animation (e.g., `diffusion_StandardWalker.gif`) in the root directory. You can change the `WALKER_TYPE` variable inside `run_simulation.py` to test different walkers.

### 2. Running with Docker

The simulation can also be run inside a container for maximum reproducibility.

1.  **Navigate to the simulation directory:**
    ```bash
    cd am215_lectures/lec04/code/diffusion
    ```

2.  **Build the Docker image:**
    ```bash
    ./docker_build.sh
    ```

3.  **Run the simulation in the container:**
    ```bash
    ./docker_run.sh
    ```
    The script mounts the current directory into the container, so the output GIF will be saved in the `am215_lectures/lec04/code/diffusion/` directory on your host machine.
