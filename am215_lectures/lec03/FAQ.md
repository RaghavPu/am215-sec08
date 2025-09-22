# Reproducibility Lecture - Frequently Asked Questions

This document contains answers to common questions that may arise from the "Reproducibility" lecture.

---

### Virtual Environments (`venv`, `uv`)

#### Why shouldn't I just use `--break-system-packages`?
This flag is a last resort, not a solution. Your operating system (like Debian, Ubuntu, or Fedora) uses its own Python environment to manage system tools (e.g., parts of the software installer or system configuration GUIs). Using `--break-system-packages` to install your project's dependencies globally can overwrite a package that a system tool depends on, potentially breaking your OS in subtle or catastrophic ways. Virtual environments (`venv`, `uv`) are the correct solution because they isolate your project's dependencies from the system's, preventing any conflicts.

#### What's the real difference between `uv` and `venv`?
- **`venv`** is a module built into Python. It's a minimalist tool that creates an isolated environment using the Python interpreter it was created with. It does one thing: create the environment. You still use `pip` to manage packages inside it.
- **`uv`** is a complete, third-party package management system written in Rust. It can do what `venv` and `pip` do, but much faster. It can create virtual environments (like `venv`), install/uninstall packages (like `pip`), and even download and manage different Python versions for you, which `venv` cannot do. Think of `uv` as a supercharged replacement for both `venv` and `pip`.

#### Can I use `uv` with a `conda` environment?
Yes, but it's generally not recommended. Conda and `pip`/`uv` are two different package management systems. While you *can* `uv pip install` into an active Conda environment, you risk creating conflicts that Conda cannot resolve. For example, `uv` might install a version of a library that breaks a non-Python dependency that Conda is managing.
**Best practice:** If you are in a Conda environment, use `conda install` or `micromamba install`. Only use `pip` or `uv` for packages that are not available in any Conda channel.

#### What does `uv pip sync` do that `uv pip install -r` doesn't?
- **`uv pip install -r requirements.txt`** is *additive*. It ensures all packages in the file are installed. If you have extra packages in your environment that aren't in the file, it leaves them alone.
- **`uv pip sync requirements.txt`** is *declarative*. It makes your environment an **exact mirror** of the file. It will install missing packages and, crucially, **uninstall** any packages that are present in the environment but *not* listed in `requirements.txt`. This is much more reproducible because it prevents "ghost dependencies" from affecting your code.

---
### Full-Stack Environments (`conda`)

#### What is a "channel" in Conda? Why is `conda-forge` so important?
A **channel** is a location (a URL) where Conda looks for packages. Think of it as a repository or an app store.
- The `defaults` channel is managed by Anaconda, Inc. and contains a curated, stable set of packages.
- **`conda-forge`** is a community-led channel with a massive collection of packages. It is often more up-to-date and has a wider variety of software than `defaults`. Because it's a single, consistent community effort, using `conda-forge` as your primary channel helps avoid dependency conflicts that can arise from mixing packages from different channels.

#### Why is `micromamba` so much faster than `conda`?
`micromamba` is a complete rewrite of the Conda package manager in C++.
- **Parallel downloads:** It can download multiple packages at once.
- **Efficient dependency solver:** It uses a much faster library (`libsolv`) to resolve dependency graphs, which is often the slowest part of a `conda` installation.
- **Standalone binary:** It's a single, self-contained executable, which makes it faster to start up and easier to install.

#### If `pip` can install `numpy` with its C libraries, why do I need `conda`?
When you `pip install numpy`, you typically download a pre-compiled "wheel" file. The creators of that wheel have already bundled a specific version of a numerical library (like OpenBLAS) inside it. So, `pip` isn't managing the C library; it's just installing a package that already has one baked in.

The problem, as highlighted in the "Dependency Iceberg" slide, is that you have no control over *which* underlying library you get. A colleague on a different OS might get a wheel with a different library (e.g., MKL instead of OpenBLAS). These different libraries can produce slightly different numerical results.

`conda` gives you explicit control over that entire software stack. As shown in the `environment.yml` example, you can pin not just `numpy`, but also the specific BLAS library, like `mkl=2023.1`. This ensures everyone on the team is using the exact same low-level libraries, which is critical for achieving bit-for-bit numerical reproducibility.

In short: `pip`/`uv` give you a *working* environment by using pre-bundled dependencies. `conda` gives you a *reproducible* scientific environment by allowing you to explicitly manage those dependencies.

#### What are MKL and OpenBLAS, and why do they give different results?
MKL (Math Kernel Library) and OpenBLAS are two different libraries that provide highly optimized implementations of Basic Linear Algebra Subprograms (BLAS) and LAPACK routines. These are the low-level workhorses for matrix multiplication, solving linear systems, etc., that libraries like NumPy and SciPy call under the hood.
- **MKL** is developed by Intel and is highly optimized for Intel CPUs.
- **OpenBLAS** is an open-source alternative that is optimized for a wide range of CPUs.
They can give slightly different results for the same operation due to using different algorithms, different orders of floating-point operations, or different levels of numerical precision internally. For most scientific work, these differences are negligible, but for achieving bit-for-bit reproducibility, you must ensure everyone is using the same BLAS library.

---
### Containers (`Docker`)

#### Can you explain "namespaces" and "cgroups" in simple terms?
Namespaces and cgroups are the two core Linux kernel features that make containers possible.
- **Namespaces** provide **isolation**. A container gets its own "view" of the system. For example, a `pid` (process ID) namespace means the container has its own process tree, starting with PID 1. A `net` namespace gives it its own network stack (its own IP address, routing tables, etc.). To the process inside the container, it looks like it's running on its own private machine.
- **Cgroups** (Control Groups) provide **resource limits**. They control how much CPU, memory, and I/O a container is allowed to use. This prevents one container from consuming all the host's resources and starving other processes.
In short: **Namespaces make a container *think* it's alone; cgroups prevent it from misbehaving.**

#### How is a container different from a VM? What is a "hypervisor"?
- A **Virtual Machine (VM)** emulates an entire physical computer. A **hypervisor** (like VirtualBox, VMware, or KVM) is the software that creates and manages VMs. It has to boot a full guest operating system (e.g., Linux on top of Windows). This is heavyweight and slow.
- A **Container** does *not* emulate hardware. It's just a regular process on the host OS that is isolated by namespaces and limited by cgroups. All containers on a host share the same host OS kernel. This is why they are so lightweight and fast to start.

| Feature | Virtual Machine | Container |
|---|---|---|
| Abstraction | Hardware | Operating System |
| Overhead | High (Full OS) | Low (Isolated Process) |
| Size | Gigabytes | Megabytes |
| Start Time | Minutes | Seconds |

#### What is a "layer" in a Docker image and why does caching matter?
Each instruction in a `Dockerfile` (like `RUN`, `COPY`, `ADD`) creates a read-only **layer** in the image. When you build an image, Docker checks if it already has a layer for a given instruction. If the instruction and the files it depends on haven't changed, Docker reuses the existing layer from its cache instead of re-running the instruction.
This is why the order in your `Dockerfile` is so important. By copying `requirements.txt` and running `pip install` *before* copying the rest of your source code, you ensure that the slow package installation step is only re-run when `requirements.txt` actually changes, not every time you edit a source file.

#### How do I share my Docker image with others? Is it free?
You share Docker images by pushing them to a **container registry**, which is a storage system for container images. Your collaborators can then pull the image from the registry. The most common workflow is:

1.  **Tag your image:** Before you can push an image, you need to tag it with the registry's address and your username:
    ```bash
    # Format: <registry>/<username>/<image_name>:<tag>
    docker tag my-app-image your-username/my-app-image:v1.0
    ```
    For Docker Hub, you can omit the registry name.

2.  **Log in to the registry:**
    ```bash
    docker login
    # For GHCR, it would be: docker login ghcr.io
    ```

3.  **Push the image:**
    ```bash
    docker push your-username/my-app-image:v1.0
    ```

**Registry Options & Costs:**
- **Docker Hub:** The default registry. It's very easy to use and offers unlimited free public repositories. There are also a limited number of free private repositories, making it a great starting point.
- **GitHub Container Registry (ghcr.io):** Excellent if your code is already on GitHub. It's free for public images associated with public repositories. Private images use your account's storage quota for GitHub Packages.
- **Cloud Registries (Amazon ECR, Google Artifact Registry, Azure ACR):** These are integrated with cloud platforms and are ideal for large-scale deployments, but typically involve storage and data transfer costs.

For most academic and open-source projects, using a free public repository on **Docker Hub** or **GitHub Container Registry** is the standard and easiest way to share your work.

---
### Advanced Topics (`Nix`, `Spack`)

#### How does Nix *actually* guarantee reproducibility? What is a "derivation"?
Nix achieves reproducibility through two core principles:
1.  **Purely Functional Builds:** A build process is treated like a pure function. Its inputs are *all* of its dependencies (source code, build tools like `gcc`, libraries like `glibc`, build scripts, etc.). The output is the final package.
2.  **Cryptographic Hashing:** Nix computes a cryptographic hash of *all* inputs. This hash is used to create a unique path in the "Nix store" (e.g., `/nix/store/<hash>-numpy-1.26.4`). The package is built and placed in that directory.

A **derivation** is a file that specifies everything needed for a build: the inputs, the build script, and the expected output hash. Because the output path depends on the hash of all inputs, any change to any input—even a single byte in a compiler flag—results in a different hash and a different output path. This prevents conflicts and guarantees that if two machines have the same path in their Nix store, they have the exact same bit-for-bit identical package.

#### If Nix is so great, why doesn't everyone use it?
Nix has a notoriously steep learning curve.
- **Declarative, Functional Paradigm:** It requires thinking about package management in a way that is very different from traditional imperative systems (`apt-get install`, `pip install`).
- **The Nix Language:** Defining packages requires learning the Nix expression language, which is a lazy, functional language that can be unfamiliar to many developers.
- **Ecosystem:** While the Nixpkgs repository is massive, integrating software that wasn't designed with Nix's strict isolation in mind can be challenging.
For these reasons, Nix is often seen as a high-investment, high-reward tool. Tools like `uv` and `conda` offer 80% of the benefits for 20% of the effort.

#### When would I use Spack instead of Conda on an HPC cluster?
Spack and Conda solve similar problems, but are designed for different use cases.
- **Conda** is user-centric. It's great for managing self-contained project environments with pre-compiled binaries.
- **Spack** is designed for HPC system administrators and users who need to build software from source with very specific configurations. Its key strength is managing "combinatorial complexity." For example, you can use Spack to build a library with a specific MPI implementation, a specific compiler version, and specific CPU optimization flags (`spack install my-app %gcc@11.2 ^openmpi@4.1.4`). This level of fine-grained control over the build process is essential in HPC but is often overkill for typical data science projects.

---
### Randomness & Numerical Stability

#### Why is `np.random.seed()` bad? I see it everywhere.
`np.random.seed()` controls NumPy's old, legacy random number generation system, which relies on a single **global state**. This means that any piece of code anywhere in your program (including in third-party libraries) that calls a function like `np.random.rand()` will advance the same hidden random number stream. This makes your results dependent on the exact order of execution, which is very fragile. A minor library update could change the number of random draws it makes internally, silently breaking your reproducibility. The modern approach (`np.random.default_rng()`) creates an isolated generator object that you pass explicitly to functions, avoiding this global state problem entirely.

#### How do I get reproducible results with parallel code (multithreading)?
Parallel code introduces non-determinism, primarily from two sources: random number generation and parallel reductions (like sums).

**1. Random Number Generation:**
You cannot have multiple threads/processes share a single random number generator (RNG), as the order in which they access it is not guaranteed. You also cannot give every worker the *same* seed, because then they would all produce the exact same sequence of random numbers.

The standard practice is to give each worker its own independent, seeded RNG. The modern NumPy library provides `np.random.SeedSequence` for this exact purpose. You create a master `SeedSequence` and then `spawn` independent child sequences from it for each worker.

```python
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def worker_function(seed_sequence):
    # Each worker creates its own independent RNG from its assigned sequence
    rng = np.random.default_rng(seed_sequence)
    # This worker's random numbers are independent of all others
    return rng.random()

# 1. Create a master SeedSequence from a single, high-entropy seed
ss = np.random.SeedSequence(12345)

# 2. "Spawn" independent child sequences for each of your N workers
child_sequences = ss.spawn(4) # Creates 4 independent sequences

# 3. Pass one child sequence to each worker
with ThreadPoolExecutor() as executor:
    results = list(executor.map(worker_function, child_sequences))

# This list of results will be identical on every run.
print(results)
```

**2. Parallel Reductions:**
Floating-point math is not associative (i.e., `(a + b) + c` is not always bit-for-bit identical to `a + (b + c)`). In a parallel sum, the order of additions is non-deterministic, which can lead to tiny variations in the final result. Achieving bit-for-bit reproducible parallel sums is difficult and often requires forcing a deterministic reduction order, which may reduce performance. For many libraries, setting an environment variable like `OMP_NUM_THREADS=1` is a "big hammer" approach that forces serial execution, ensuring reproducibility at the cost of parallelism.

#### What is floating-point error and why can't I just use `==` to compare floats?
Computers cannot represent most decimal numbers exactly in binary. They use an approximation called a floating-point number. This leads to tiny rounding errors. For example, `0.1 + 0.2` is not exactly `0.3` in binary; it's `0.30000000000000004`.
Because of these small precision errors, using `==` to compare the results of floating-point calculations is unreliable. Two computations that are mathematically identical might produce results that differ by a tiny amount. The correct way to compare floats is to check if they are "close enough" by testing if the absolute difference is within a small tolerance: `abs(a - b) < tolerance`. NumPy provides `np.isclose()` for this purpose.
