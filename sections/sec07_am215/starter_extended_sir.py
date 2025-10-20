# Starter template for the extended SIR model with vaccination, hospitalisation,
# and mortality dynamics. Fill in the TODOs in `extended_sir_model`.

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


def extended_sir_model(y, t, beta, alpha, gamma, delta, p_h, eta, mu, mu_h, nu, omega):
    """
    Compute derivatives for the extended SIR model with vaccination and hospitalisation.

    Parameters
    ----------
    y : sequence[float]
        Current compartment sizes in the order (S, V, I, H, R, D).
    t : float
        Time (in days). Required by `odeint` even though the system is autonomous.
    beta : float
        Baseline transmission rate for susceptible individuals.
    alpha : float
        Relative transmission scaling for vaccinated individuals (alpha < 1 reduces transmission).
    gamma : float
        Recovery rate for infected individuals.
    delta : float
        Rate at which infected individuals transition to the hospitalised compartment.
    p_h : float
        Proportion of infected individuals who require hospitalisation.
    eta : float
        Recovery rate for hospitalised individuals.
    mu : float
        Mortality rate for infected individuals outside the hospital.
    mu_h : float
        Mortality rate for hospitalised individuals.
    nu : float
        Vaccination rate among susceptible individuals.
    omega : float
        Rate at which recovered individuals lose immunity and return to susceptible.

    Returns
    -------
    tuple[float, float, float, float, float, float]
        Time derivatives dS/dt, dV/dt, dI/dt, dH/dt, dR/dt, dD/dt.

    Notes
    -----
    - Susceptible individuals can become infected, vaccinated, or regain susceptibility via waning immunity.
    - Vaccinated individuals have reduced transmission (`alpha`) but can still be infected.
    - Infected individuals recover, die, or move into hospitalisation at rate `p_h * delta`.
    - Hospitalised individuals recover at rate `eta` or die at rate `mu_h`.
    - Deceased individuals accumulate mortality contributions from both infected and hospitalised classes.
    """
    S, V, I, H, R, D = y
    N = S + V + I + H + R

    # TODO: Replace the placeholder with the system of ODEs for the extended SIR model.
    # dSdt = ...
    # dVdt = ...
    # dIdt = ...
    # dHdt = ...
    # dRdt = ...
    # dDdt = ...
    raise NotImplementedError("Implement the extended SIR model derivatives before running the simulation.")


def simulate_extended_sir(y0, t, params):
    """Integrate the extended SIR model forward in time."""
    args = (
        params["beta"],
        params["alpha"],
        params["gamma"],
        params["delta"],
        params["p_h"],
        params["eta"],
        params["mu"],
        params["mu_h"],
        params["nu"],
        params["omega"],
    )
    return odeint(extended_sir_model, y0, t, args=args)


def plot_trajectories(t, trajectory):
    """Plot compartment trajectories for the extended SIR simulation."""
    S, V, I, H, R, D = trajectory.T
    plt.figure(figsize=(8, 5))
    plt.plot(t, S, label="Susceptible", linewidth=2)
    plt.plot(t, V, label="Vaccinated", linewidth=2)
    plt.plot(t, I, label="Infected", linewidth=2)
    plt.plot(t, H, label="Hospitalised", linewidth=2)
    plt.plot(t, R, label="Recovered", linewidth=2)
    plt.plot(t, D, label="Deceased", linewidth=2)
    plt.xlabel("Time (days)")
    plt.ylabel("Number of People")
    plt.title("Extended SIR Model Simulation")
    plt.grid(alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    params = {
        "beta": 0.5,   # Mean transmission rate.
        "alpha": 0.5,  # Relative transmission reduction for vaccinated individuals.
        "gamma": 0.1,  # Mean recovery rate (in 1/days).
        "delta": 0.05,  # Hospitalisation rate for infected individuals (in 1/days).
        "p_h": 0.1,    # Proportion of infected individuals who are hospitalised.
        "eta": 0.03,   # Recovery rate for hospitalised individuals (in 1/days).
        "mu": 0.01,    # Mortality rate for infected individuals (in 1/days).
        "mu_h": 0.02,  # Mortality rate for hospitalised individuals (in 1/days).
        "nu": 0.01,    # Vaccination rate (in 1/days).
        "omega": 0.001,  # Immunity waning rate (in 1/days).
    }

    N = 10000  # Total population.
    I0, R0 = 1, 0  # Initial infected and recovered individuals.
    V0, H0, D0 = 0, 0, 0  # Initial vaccinated, hospitalised, and deceased individuals.
    S0 = N - I0 - R0 - V0 - H0 - D0  # Everyone else starts susceptible.
    initial_conditions = [S0, V0, I0, H0, R0, D0]

    time_grid = np.linspace(0, 160, 300)

    solution = simulate_extended_sir(initial_conditions, time_grid, params)
    plot_trajectories(time_grid, solution)
