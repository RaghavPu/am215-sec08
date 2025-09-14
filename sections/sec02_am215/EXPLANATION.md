# Hypersphere Volume Estimation — Explanation and Interpretation

This note explains the mathematical setup of the experiment, what each script does, and how to interpret the resulting plots.

---

## 1) Problem Setup

We estimate the volume of the **unit d-dimensional ball**:
$$
B_d = \{\, x \in \mathbb{R}^d : \|x\|_2 \le 1 \,\}.
$$

Its true volume is
$$
V_d = \frac{\pi^{d/2}}{\Gamma\!\left(\tfrac{d}{2}+1\right)}.
$$

For reference:
- $V_2 = \pi \approx 3.1416$
- $V_3 = \tfrac{4\pi}{3} \approx 4.1888$
- $V_4 = \tfrac{\pi^2}{2} \approx 4.9348$

---

## 2) Monte Carlo Estimator

We sample points uniformly from the cube $[-1,1]^d$ (whose volume is $2^d$), count how many fall inside $B_d$, and scale by the cube volume.

Let $N$ be the total samples and $K_N$ the count inside the ball. The estimator is:
$$
\hat V_d(N) = 2^d \cdot \frac{K_N}{N}.
$$

This estimator is unbiased:
$$
\mathbb{E}[\hat V_d(N)] = V_d.
$$

If $p = \Pr(\text{point in }B_d) = V_d/2^d$, then
$$
\operatorname{Var}\!\left(\hat V_d(N)\right) = \frac{2^{2d}}{N}\, p(1-p),
\qquad
\operatorname{SE}\!\left(\hat V_d(N)\right) \propto \frac{1}{\sqrt{N}}.
$$

**Implications**
- Increasing $N$ reduces standard error like $1/\sqrt{N}$.
- As $d$ grows, $p = V_d/2^d$ gets small, so it takes more samples to achieve the same precision.

---

## 3) What the Scripts Do

- **`hypersphere_volume.py`**  
  For a given dimension and max sample size, it draws points and prints lines like  
  `dimension,num_points,estimate,true_volume`  
  at logarithmically spaced values of `num_points`.

- **`volume_estimator.sh`**  
  Prompts for inputs and appends multiple runs to `results.csv`. (No git actions.)

- **`visualize_results.py`**  
  Reads `results.csv`, groups by `num_points`, computes the mean and standard deviation of the estimates, and makes a two-panel plot per dimension.

---

## 4) Interpreting the Plots

Each `volume_estimate_<d>D.png` has two panels.

### Left Panel — Estimate vs. N (x-axis log scale)
- **Red horizontal line:** the true volume $V_d$.
- **Black dashed curve:** the mean Monte Carlo estimate at each $N$.
- **Gray band:** $\pm 1$ standard deviation across simulations at each $N$.

**What to look for:**  
The black curve should fluctuate around the red line and the gray band should **shrink** as $N$ increases, reflecting the $1/\sqrt{N}$ variance decay.

### Right Panel — Absolute Error vs. N (log–log)
- **Black dashed curve:** $|\hat V_d(N) - V_d|$.
- **Red reference line:** proportional to $1/\sqrt{N}$, normalized to the first point.

**What to look for:**  
On a log–log plot, a $1/\sqrt{N}$ trend appears as an approximately straight line with slope $-1/2$. The black curve tracking roughly parallel to the red line confirms the expected Monte Carlo error scaling.

---

## 5) Why Higher Dimensions Are Harder

The fraction of the cube occupied by the ball,
$$
p = \frac{V_d}{2^d},
$$
drops rapidly with $d$. With fewer hits per fixed $N$, the estimator has higher variance, so more samples are needed to achieve the same accuracy.

---

## 6) Takeaways

- The estimator $\hat V_d(N)$ is simple, unbiased, and dimension-agnostic.
- Precision improves like $1/\sqrt{N}$, visible as narrowing uncertainty on the left panel and a $-1/2$ slope on the right panel.
- In higher dimensions, expect to use larger $N$ to see the same quality of convergence.
