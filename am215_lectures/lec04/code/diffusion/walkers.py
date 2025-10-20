import random
from abc import ABC, abstractmethod

class RandomWalker(ABC):
    """An abstract base class defining the walker API contract."""
    WALKER_REGISTRY = {}

    def __init_subclass__(cls, **kwargs):
        """
        Called when a class inherits from this one.
        This method registers the new walker type in a central registry.
        """
        super().__init_subclass__(**kwargs)
        # Don't register the base class itself
        if cls.__name__ != 'RandomWalker':
            RandomWalker.WALKER_REGISTRY[cls.__name__] = cls
        print(f"Registered walker: {cls.__name__}")

    @abstractmethod
    def move(self, particle):
        """Move the particle according to the walker's rules."""
        pass

class StandardWalker(RandomWalker):
    """A simple walker that takes a random step in any direction."""
    def move(self, particle):
        particle.x += random.uniform(-1, 1)
        particle.y += random.uniform(-1, 1)

class BiasedWalker(RandomWalker):
    """A walker that tends to move to the right."""
    def move(self, particle):
        particle.x += random.uniform(0, 2)  # Biased step to the right
        particle.y += random.uniform(-1, 1)
