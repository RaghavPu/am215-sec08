# AM215 Section 6: Extreme Value Distributions

In this section, you'll explore extreme value statistics, the mathematical theory describing the behavior of maxima (or minima) in random samples. You'll see how different base distributions lead to universal extreme value distributions (EVDs), verify theoretical scaling predictions, and apply this framework to real marathon data.

We will do this through a class-based API following Python data model principles, moving from standalone functions to reusable, composable objects.

---

## Learning Goals
- Understand how extreme value distributions emerge from repeated sampling of IID variables
- Implement class-based APIs for statistical analysis (Python Data Model)
- Verify theoretical predictions about scaling behavior (mean ~ sqrt(log N))
- Recognize universality: different base distributions lead to same EVD shape
- Fit Gumbel distributions and assess goodness of fit
- Apply EVD theory to real-world data and understand its limitations

---

## What's in this section directory

    distributions.py            # Base distribution classes (Gaussian, Exponential)
    evd_analyzer.py             # EVDAnalyzer class for computing maxima distributions
    analyze_scaling.py          # Script to study how mean/std scale with sample size
    gumbel_fitter.py            # GumbelFitter class for fitting and visualization
    marathon_analyzer.py        # MarathonData class for real data analysis
    data/
        nyc_marathon.csv        # NYC Marathon winning times dataset (1970-2020)
    requirements.txt            # Project dependencies
    README.md                   # This file

You will complete TODOs in key methods and answer conceptual questions throughout.

---

## Prerequisites
- **Python 3.9+**
- **Git**
- **macOS/Linux:** Terminal (bash/zsh)
- **Windows:**  
  - PowerShell for Python environment setup  
  - **Git Bash** (installed with Git for Windows) to run `*.sh` scripts

---

## 0) Clone & set up Python

### macOS / Linux — Terminal

```bash
git clone https://code.harvard.edu/AM215/main_2025.git
cd main_2025/sections/sec06_am215

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt
python3 -c "import numpy, pandas, matplotlib, scipy; print('Dependencies OK')"
```

### Windows — PowerShell

```powershell
git clone https://code.harvard.edu/AM215/main_2025.git
cd main_2025\sections\sec06_am215

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -c "import numpy, pandas, matplotlib, scipy; print('Dependencies OK')"
```

---

## 1) Build Empirical Extreme Value Distributions

In this step, you'll implement classes for sampling from base distributions and computing empirical EVDs. This demonstrates object-oriented design for statistical analysis.

### Files to examine and edit:
- `distributions.py` - Abstract base class and concrete samplers
- `evd_analyzer.py` - Class to compute maxima distributions

### TODO:
In `evd_analyzer.py`, complete the `compute_maxima()` method to generate batched maxima using the distribution sampler.

### Run:

```bash
python3 evd_analyzer.py
```

You should see histograms comparing the EVD from Gaussian samples to the original Gaussian distribution.

### Question to consider:

**Q1**: The probability that the maximum of n samples is less than z is P(M_n ≤ z) = C(z)^n, where C(z) is the cumulative distribution of the base distribution. Using this formula, explain why the extreme value distribution becomes more concentrated (narrower) as n increases.

---

## 2) Analyze Scaling Behavior of Extrema

Theory predicts that for Gaussian samples, the mean of maxima scales approximately as σ√(log N), where N is the sample size. You'll verify this empirically.

### Files to run:
- `analyze_scaling.py` - Uses `EVDAnalyzer` to study scaling

### What happens:

The script generates maxima for various sample sizes N (from ~10 to 1,000,000) and plots:
1. Mean of maxima vs. N (log scale)
2. Standard deviation of maxima vs. N (log scale)  
3. Mean vs. √(log N) with linear fit

### Run:

```bash
python3 analyze_scaling.py
```

### Question to consider:

**Q2**: The fitted relationship shows mean ≈ a√(log N) + b with a ≈ 1.5. For a standard Gaussian (σ=1), theory predicts a ≈ √2 ≈ 1.414. Derive this relationship by considering where the tail probability e^(-x²/2) equals 1/N.

---

## 3) Demonstrate Universality and Fit Gumbel Distribution

Different base distributions (Gaussian, Exponential) with fast-decaying tails all lead to the same *shape* of EVD—the Gumbel distribution. This is an example of universality in statistics.

### Files to examine and edit:
- `gumbel_fitter.py` - Class for fitting and visualizing Gumbel distributions

### TODO:
Complete the `plot_fit()` method in `GumbelFitter` to create a histogram of data and overlay the fitted Gumbel PDF.

### Run:

```bash
python3 gumbel_fitter.py
```

You should see:
- Z-score histograms showing collapse of Gaussian and Exponential EVDs
- Fitted Gumbel distributions overlaid on raw maxima

### Question to consider:

**Q3**: After standardizing to z-scores, the EVDs from Gaussian and Exponential bases collapse onto nearly the same curve, both well-fit by a Gumbel distribution. This is universality. The Fisher-Tippett theorem says there are exactly 3 universality classes: Gumbel (for thin tails), Fréchet (for power-law tails), and Weibull (for bounded distributions). Explain what property of the base distribution determines which class applies.

---

## 4) Analyze Real Marathon Data

Apply EVD theory to NYC Marathon winning times (1970-2020). Since we're interested in the *fastest* (minimum) times, we use the left-skewed Gumbel distribution. We analyze Men's and Women's divisions separately to avoid mixing different populations.

### Files to examine and edit:
- `marathon_analyzer.py` - Class for loading, cleaning, and analyzing marathon data
- `data/nyc_marathon.csv` - Real NYC Marathon results (1970-2020)

### TODOs:
1. Complete `parse_time()` method to convert time strings (format "hh:mm:ss") to seconds
2. Implement `yearly_best` property to extract the minimum time for each year

### Run:

```bash
python3 marathon_analyzer.py
```

You should see:
- Summary statistics for Men's and Women's divisions separately
- Side-by-side histograms with fitted Gumbel_L distributions

### Question to consider:

**Q4**: The Gumbel distribution assumes that yearly winning times are IID (independent and identically distributed) samples. Are they really? Consider how training methods, shoe technology, course changes, athlete selection, and other factors have evolved from 1970 to 2020. What would be the consequences of these violations on our fitted model and predictions?

---

## Troubleshooting

- **`python` vs `python3`**  
  If `python3` isn't found on macOS/Linux, try `python`. If `python` points to Python 2 (rare), install Python 3.

- **Import errors**  
  Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

- **Plots don't appear**  
  If running in a remote environment, plots save to disk but may not display. Check for `.png` files in the directory.

- **Data file not found**  
  Ensure you're running scripts from the `sec06_am215/` directory, not from the repo root.

---

## Wrap-Up

You've explored how extreme value statistics arise from fundamental probability theory, verified theoretical predictions through simulation, and applied the framework to real data. You've also practiced designing class-based APIs that encapsulate statistical workflows.

There is no submission for this section. If you want to explore further, try applying EVD analysis to a different dataset (rainfall, stock returns, network traffic, etc.).
