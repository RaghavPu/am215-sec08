import math

class Particle:
    """Represents a single particle with a position in 2D space."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Particle(x={self.x:.2f}, y={self.y:.2f})"

    @property
    def r(self):
        """The particle's distance from the origin (polar coordinate r)."""
        return math.sqrt(self.x**2 + self.y**2)

    @r.setter
    def r(self, new_r):
        """
        Scales the particle's position to a new radius, preserving its angle.
        """
        if self.r == 0:
            # Cannot determine angle if at origin, do nothing.
            return
        ratio = new_r / self.r
        self.x *= ratio
        self.y *= ratio

    @property
    def theta(self):
        """The particle's angle in radians (polar coordinate theta)."""
        return math.atan2(self.y, self.x)
