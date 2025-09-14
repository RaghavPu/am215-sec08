# AM215 Section: Monte Carlo & Git — Hypersphere Volumes

In this section you’ll run and read a small Monte Carlo project while practicing a few core Git actions.  
There is no deliverable and no file editing required. The focus is understanding how the scripts work and how commits/branches record work over time.

---

## Learning Goals
- See a Monte Carlo estimator for the volume of a hypersphere and how error scales like $1/\sqrt{N}$.
- Practice basic Git: clone, branch, switch, merge, and inspect history.

---

## What’s in this section directory

    hypersphere_volume.py       # Monte Carlo estimator (prints CSV rows)
    visualize_results.py        # Reads results.csv and makes plots
    volume_estimator.sh         # Driver that prompts, runs the estimator and appends to results.csv,
    .gitignore                  # Already ignores *.png
    requirements.txt            # Handles project dependencies (more on this in the coming weeks)
    README.md                   # This file

You should not modify any files. The driver script will create `results.csv` and commit it for you.

---

## Prerequisites
- **Python 3.9+**
- **Git**
- **macOS/Linux:** Terminal (bash/zsh)
- **Windows:**  
  - PowerShell for Python environment setup  
  - **Git Bash** (installed with Git for Windows) to run `*.sh` scripts

---

## What to read

- **`hypersphere_volume.py`**  
  Prints CSV rows: `dimension,num_points,estimate,true_volume` at logarithmically spaced `num_points`.  
  Skim how the inside-the-ball check and estimate are computed.

- **`volume_estimator.sh`**  
  Prompts for inputs, loops simulations, and appends to `results.csv`.

- **`visualize_results.py`**  
  Groups by `num_points`, plots the MC mean and std bands, and an error curve against \(N\).

  OPTIONAL: read `EXPLANATION.md` for the math behind the experiment.

## 0) Clone & set up Python

### macOS / Linux — Terminal

    git clone https://code.harvard.edu/AM215/main_2025.git
    cd main_2025/sections/sec02_am215

    python3 -m venv venv
    source venv/bin/activate

    python3 -m pip install -r requirements.txt
    python3 -c "import numpy, pandas, matplotlib; print('ok')"

### Windows — PowerShell (for environment), then Git Bash (for *.sh)

    git clone https://code.harvard.edu/AM215/main_2025.git
    cd main_2025\sections\sec02_am215

    python -m venv venv
    .\venv\Scripts\Activate.ps1

    python -m pip install -r requirements.txt
    python -c "import numpy, pandas, matplotlib; print('ok')"

Now **open Git Bash** in the same folder, then activate the venv inside Git Bash:

    source venv/Scripts/activate

From here on:
- **macOS/Linux:** keep using Terminal.  
- **Windows:** keep using **PowerShell** for git/Python, use **Git Bash** when explicitly instructed to.

---

## 1) Quick Git Warm-up

Create a branch, switch to it, then you’ll make a commit there in Step 2.

    git checkout main
    git branch improvement
    git checkout improvement

You are now on the `improvement` branch.

---

## 2) Generate results with the driver (minimal typing)

Run the driver. It will prompt for inputs, call the estimator, and **append** to `results.csv`.  
It does **not** perform any git actions; you will commit manually.

Run (macOS/Linux Terminal or Windows Git Bash):

    ./volume_estimator.sh

If you see a permissions error:

    chmod +x volume_estimator.sh
    ./volume_estimator.sh

Suggested first run (fast):
- Dimension: `2` or `3`
- Max points: `100000`
- Number of simulations: `3`

Verify data was written:

    head -n 10 results.csv

Now **stage and commit your results manually** on the `improvement` branch:

    git add results.csv
    git commit -m "Add results for 2D estimation (3 sims, max 100k points)"

---

## 3) Merge your branch

Once you’ve created at least one commit on `improvement`, merge it back into `main`:

    git checkout main
    git merge improvement
    git log --oneline --graph --decorate --max-count=10

You should see your commit(s) in the `main` history.

---

## 4) Visualize the results

The plot script reads `results.csv` and writes one PNG per dimension.

    python3 visualize_results.py   # macOS/Linux
    python visualize_results.py    # Windows Git Bash

You should see files like:

    volume_estimate_2D.png
    volume_estimate_3D.png

`.gitignore` already ignores `*.png`, so images won’t show up as untracked files.

Open the images and inspect:
- Left plot: MC estimates vs. number of points (log scale), true volume line, and ±1 std shading.
- Right plot: error vs. $N$ on log–log axes; look for the ~$1/\sqrt{N}$ trend.

---

## 5) What to notice

Questions to think about:
- How does the estimate’s variance shrink as $N$ grows?
- How does dimensionality affect difficulty?
- What does the Git history tell you about your workflow?

---

## Troubleshooting

- **`python` vs `python3`**  
  If `python3` isn’t found on macOS/Linux, try `python`. If `python` points to Python 2 (rare), install Python 3.

- **Permission denied for `volume_estimator.sh`**  
  Run `chmod +x volume_estimator.sh` (macOS/Linux/Git Bash), then run again.

- **Windows can’t run the shell script in PowerShell**  
  Use **Git Bash** for the `*.sh` driver. Keep the Python venv active in Git Bash with `source venv/Scripts/activate`.

- **Plots didn’t appear**  
  Ensure `results.csv` exists and has rows (run the driver first), then run the visualize script again.

---

## Wrap-Up

You’ve run a Monte Carlo estimator, visualized convergence, and captured your work in Git with a branch and merge. There is no submission for this section. If you want to explore further, rerun the driver with different dimensions or larger `max_points`, regenerate plots, and see how the error changes.