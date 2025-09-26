import math

class Vector:
    """A simple class representing a 2D vector."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """Return an unambiguous string representation."""
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        """Defines behavior for the `+` operator (vector addition)."""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """Defines behavior for the `+=` operator (in-place addition)."""
        if not isinstance(other, Vector):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __neg__(self):
        """Defines behavior for the unary `-` operator (additive inverse)."""
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        """Defines behavior for `vector * scalar`."""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """Defines behavior for `scalar * vector`."""
        return self.__mul__(scalar)

    def __matmul__(self, other):
        """Defines behavior for the `@` operator (dot product)."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y

    @property
    def magnitude(self):
        """A read-only computed property for the vector's magnitude."""
        return math.sqrt(self.x**2 + self.y**2)
