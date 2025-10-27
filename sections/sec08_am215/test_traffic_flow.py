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
        # TODO: Implement a test for steady state conditions
        # When cars are evenly spaced with desired spacing d0 and same velocity,
        # the velocity derivatives should be zero (no acceleration)
        pass


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
