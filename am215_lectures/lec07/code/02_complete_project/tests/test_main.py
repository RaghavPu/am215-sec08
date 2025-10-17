import numpy as np
import pytest
from my_package.main import compute_mean_std

def test_compute_mean_std():
    """Tests the compute_mean_std function with a simple array."""
    data = np.array([0, 10])
    mean, std = compute_mean_std(data)
    assert mean == 5.0
    assert std == 5.0

def test_compute_mean_std_raises_error():
    """Tests that a TypeError is raised for invalid input."""
    with pytest.raises(TypeError):
        compute_mean_std([1, 2, 3]) # Passing a list, not a numpy array
