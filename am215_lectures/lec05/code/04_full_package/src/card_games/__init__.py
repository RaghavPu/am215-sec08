# Expose key classes at the top level of the package
from .deck import Deck, Card
from .game import BlackjackGame, JokerBlackjackGame
from .simulation import main as run_simulation

# Expose the version of the package
try:
    from ._version import version as __version__
except ImportError:
    # Fallback for when the package is not installed
    __version__ = "0.0.0-dev"
