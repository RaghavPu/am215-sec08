import random

class Card:
    """A single playing card with a rank and suit."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"Card('{self.rank}', '{self.suit}')"

class Deck:
    """A container for cards that behaves like a Python sequence."""
    RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    SUITS = '♠ ♡ ♢ ♣'.split()

    def __init__(self):
        """Initializes a standard 52-card deck."""
        self._cards = [Card(r, s) for s in self.SUITS for r in self.RANKS]

    def __len__(self):
        """Enables the `len()` built-in function."""
        return len(self._cards)

    def __getitem__(self, position):
        """Enables indexing, slicing, and iteration."""
        return self._cards[position]

    def shuffle(self):
        """Shuffles the cards in this deck in-place."""
        random.shuffle(self._cards)

    def draw(self):
        """Removes and returns the top card from this deck."""
        return self._cards.pop()

    @classmethod
    def create_deck_with_joker(cls):
        """A factory method to create a 53-card deck with a Joker."""
        deck = cls()  # Creates a new standard deck instance
        deck._cards.append(Card('Joker', '🃏'))
        return deck
