# Extended SIR Model Task

This exercise focuses on expanding the classical Susceptible–Infected–Recovered (SIR) epidemiological model to include vaccinated (V), hospitalised (H), and deceased (D) compartments. You will complete the implementation in `starter_extended_sir.py`, simulate the model, and reason about how these additional flows alter the disease dynamics.

## 1. Environment Setup
1. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

If you prefer using the shared conda environment, activate it instead:
```bash
conda activate env
pip install -r requirements.txt
```

## 2. Task Overview
Your goal is to update the SIR model so that it tracks six compartments: susceptible (S), vaccinated (V), infected (I), hospitalised (H), recovered (R), and deceased (D). Vaccination, hospitalisation, mortality, and waning immunity are all explicitly modelled.

Complete the following steps inside `starter_extended_sir.py`:
- Implement the system of differential equations within `extended_sir_model`. The docstring and inline comments describe the intended transitions between compartments.
- Inspect and optionally tweak the initial conditions or parameter values (`beta`, `alpha`, `gamma`, `delta`, `p_h`, `eta`, `mu`, `mu_h`, `nu`, `omega`) to explore alternative outbreak scenarios.
- Optionally adjust the plotting routine to emphasise the compartments you care about once the model runs end-to-end.

The starter script will raise `NotImplementedError` until all TODOs are addressed.

### Default Parameters
The starter code includes the following baseline values. Adjust them to explore alternative scenarios once your implementation is complete.

```python
# Mean transmission rate.
beta = 0.5

# Relative transmission reduction for vaccinated individuals.
alpha = 0.5  # Vaccinated individuals are half as likely to get infected.

# Mean recovery rate (in 1/days).
gamma = 0.1

# Hospitalisation rate for infected individuals (in 1/days).
delta = 0.05

# Proportion of infected individuals who are hospitalised.
p_h = 0.1

# Recovery rate for hospitalised individuals (in 1/days).
eta = 0.03

# Mortality rate for infected individuals (in 1/days).
mu = 0.01

# Mortality rate for hospitalised individuals (in 1/days).
mu_h = 0.02  # Higher mortality rate for hospitalised individuals.

# Vaccination rate (in 1/days).
nu = 0.01

# Immunity waning rate (in 1/days).
omega = 0.001

# Total population.
N = 1000

# Initial infected and recovered individuals.
I0, R0 = 1, 0

# Initial vaccinated, hospitalised, and deceased individuals.
V0, H0, D0 = 0, 0, 0

# Everyone else starts susceptible.
S0 = N - I0 - R0 - V0 - H0 - D0

# Initial conditions vector (used in the solver).
y0 = [S0, V0, I0, H0, R0, D0]
```

## 3. Running the Simulation
After completing the TODOs, run:
```bash
python starter_extended_sir.py
```

You should see a plot of compartment trajectories and summary statistics printed to the console. Use these outputs to reason about the effect of vaccination, hospitalisation, mortality, and waning immunity relative to the baseline SIR assumptions.

## 4. Extension Ideas (Optional)
- Experiment with different parameter values (e.g., faster vaccination, higher mortality) to see how they reshape the curves.
- Introduce interventions such as time-varying transmission rates or adaptive hospital capacity and study their impact on the outbreak.
- Try fitting the parameters to a small synthetic or real dataset using least squares minimisation.

## 5. Troubleshooting
- Ensure you activated the virtual environment before installing dependencies.
- If the solver struggles to converge, start with smaller simulation horizons or adjust step sizes.
- If the plot does not display, make sure you have a GUI backend available (or save the figure using `plt.savefig`).

Good luck, and have fun exploring richer epidemiological dynamics!
