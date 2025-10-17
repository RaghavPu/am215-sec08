import os  # Unused import, will be flagged by ruff
import numpy as np
from typing import Optional

# This function has a classic linting error.
# `ruff check` will flag the use of a mutable default argument.
def append_to(item, target=[]):
    target.append(item)
    return target

def get_user_id(user_name: str) -> Optional[int]:
    """
    A function with a type error that `ty` will catch.
    It's annotated to return an Optional[int], but it returns a string.
    """
    if user_name == "admin":
        return "ADMIN_ID_001" # Incorrect return type
    return None

def compute_mean_std(data: np.ndarray) -> tuple[float, float]:
    """Computes the mean and standard deviation of an array.

    This function serves as an example for documentation and testing.

    Parameters
    ----------
    data : np.ndarray
        A NumPy array of numerical data.

    Returns
    -------
    tuple[float, float]
        A tuple containing the mean and standard deviation of the data.

    Examples
    --------
    >>> import numpy as np
    >>> d = np.array([1, 2, 3, 4, 5])
    >>> mean, std = compute_mean_std(d)
    >>> round(mean, 2)
    3.0
    >>> round(std, 2)
    1.41
    """
    if not isinstance(data, np.ndarray):
        raise TypeError("Input must be a NumPy array.")
    
    mean = np.mean(data)
    std = np.std(data)
    
    return mean, std
