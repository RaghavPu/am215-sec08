import sys
import os

# This is an anti-pattern! Do not do this in real projects.
# It makes the script dependent on a specific, fragile directory structure.
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)

from card_games.deck import Deck

print("--- Demo 1: sys.path hack ---")
print("Successfully imported 'Deck' by modifying sys.path.")
deck = Deck()
print(f"Created a deck with {len(deck)} cards.")
