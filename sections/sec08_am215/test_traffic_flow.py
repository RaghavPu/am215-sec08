#!/usr/bin/env python3
"""
Test suite for the car-following traffic flow model.

Complete the TODO to implement a test for the car_following_ode function.
"""

import pytest
import numpy as np
from scipy.integrate import solve_ivp
from traffic_flow import car_following_ode


class TestCarFollowingODE:
    """Test cases for the car_following_ode function."""
    
    def test_basic_functionality(self):
        """Test that the function returns the correct shape and type."""
        ncars = 5
        y = np.ones(2*ncars-1)
        t = 0.0
        
        result = car_following_ode(t, y, ncars)
        
        assert isinstance(result, np.ndarray)
        assert result.shape == (2*ncars-1,)
        assert np.all(np.isfinite(result))
    
    def test_steady_state(self):
        """Test behavior when cars are properly spaced."""
        # When cars are evenly spaced with desired spacing d0 and same velocity,
        # the velocity derivatives should be zero (no acceleration)
        ncars = 5
        d0 = 1.0  # desired spacing
        
        # Set up initial state: cars evenly spaced with spacing d0
        # Positions: [5, 4, 3, 2, 1] (spacing of 1 between consecutive cars)
        positions = np.arange(ncars, 0, -1, dtype=float)
        
        # All cars moving at the same velocity
        velocities = np.ones(ncars - 1) * 2.0  # following cars all at velocity 2.0
        
        # Construct the state vector [x1, x2, ..., xn, v2, v3, ..., vn]
        y = np.concatenate([positions, velocities])
        
        # Define a constant velocity for the leading car
        def leading_car_velocity(t):
            return 2.0
        
        t = 0.0
        result = car_following_ode(t, y, ncars, d0=d0, leading_car_velocity=leading_car_velocity)
        
        # Position derivatives should equal velocities (first ncars elements)
        position_derivatives = result[:ncars]
        expected_velocities = np.array([2.0, 2.0, 2.0, 2.0, 2.0])
        np.testing.assert_allclose(position_derivatives, expected_velocities, rtol=1e-5)
        
        # Velocity derivatives should be zero (cars are at desired spacing)
        velocity_derivatives = result[ncars:]
        np.testing.assert_allclose(velocity_derivatives, np.zeros(ncars - 1), atol=1e-6)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
