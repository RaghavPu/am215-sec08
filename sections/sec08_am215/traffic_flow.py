#!/usr/bin/env python3
"""
Traffic Flow Simulation using the Car-Following Model

Complete the TODOs to implement the car-following model and visualize traffic dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Configuration for the plots
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['xtick.bottom'] = True
plt.rcParams['ytick.left'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['figure.titlesize'] = 20


def car_following_ode(t, y, ncars, d0=1, leading_car_velocity=None):
    """
    Computes the derivatives for the car-following model.
    
    This function implements the differential equations:
    - dx_i/dt = v_i (position changes according to velocity)
    - dv_i/dt = λ((x_{i-1} - x_i) - d₀) (velocity changes according to car-following rule)
    
    Parameters:
    -----------
    t : float
        Current time
    y : array
        State vector [x1, x2, ..., xn, v2, v3, ..., vn] (positions and velocities)
    ncars : int
        Number of cars
    d0 : float
        Desired spacing between cars
    leading_car_velocity : callable or None
        Function that returns leading car velocity at time t
        
    Returns:
    --------
    dydt : array
        Time derivatives of the state vector
    """
    # Reading out the position and speeds of the cars from the y vector
    position = np.array(y[:ncars])
    
    # Initialize the velocity
    speed = np.zeros((ncars,), dtype=np.float32)
    
    # Leading car velocity is prescribed and not part of the solution
    if leading_car_velocity is None:
        speed[0] = 1. + np.random.normal()*0.01 
    else: 
        speed[0] = leading_car_velocity(t)
    
    # The speeds of the following cars are given by the last ncars-1 component of the y vector        
    speed[1:] = np.array(y[ncars:]) 
    
    # Initialize the derivatives
    dydt = np.zeros((2*ncars-1,), dtype=np.float32)
    
    # TODO: Calculate acceleration for each following car based on car-following rule
    
    # TODO: Set the derivatives
    # dydt[:ncars] = ? (position derivatives)
    # dydt[ncars:] = ? (velocity derivatives)

    return dydt


def main():
    """Run traffic flow simulation and visualization."""
    
    # Initial conditions
    # Number of cars
    ncars = 10
    # Total simulation time
    t_sim = 20
    # Initial positions
    y0 = np.ones((2*ncars-1,), dtype=np.float32)
    y0[:ncars] = np.array(range(ncars, 0, -1), dtype=np.float32)
    
    # Solve the equation by integrating
    sol = solve_ivp(car_following_ode, [0, t_sim], y0, args=[ncars], max_step=0.1)
    
    # Plot the positions and velocities as function of time
    fig, axs = plt.subplots(nrows=3, figsize=(12, 16))
    
    # Create a color gradient for plotting all solutions
    colors_pos = plt.cm.cividis(np.linspace(0., 1., ncars))
    colors_vel = plt.cm.plasma(np.linspace(0., 1., ncars - 1))
    
    # Plot car positions over time
    for car in range(ncars):
        axs[0].plot(sol.t, sol.y[car, :], color=colors_pos[car])
    axs[0].set(xlabel='time', ylabel='car position')
    axs[0].set_title('Car Positions vs Time')
    axs[0].grid(True, alpha=0.3)
    
    # Plot velocities over time
    for car in range(ncars - 1):
        axs[1].plot(sol.t, sol.y[ncars + car, :], color=colors_vel[car])
    axs[1].set(xlabel='time', ylabel='velocity')
    axs[1].set_title('Car Velocities vs Time')
    axs[1].grid(True, alpha=0.3)
    
    # Plot car position vs velocity at the final time step
    final_time_index = -1  # Last time step
    axs[2].plot(sol.y[1:ncars, final_time_index], sol.y[ncars:, final_time_index], '-o')
    axs[2].set_title(r'$t = %.1f$' % sol.t[final_time_index])
    axs[2].set(xlabel='car position', ylabel='velocity')
    axs[2].set_title('Phase Space at Final Time')
    axs[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('traffic_simulation.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Traffic simulation complete. Plot saved as 'traffic_simulation.png'")


if __name__ == "__main__":
    main()
