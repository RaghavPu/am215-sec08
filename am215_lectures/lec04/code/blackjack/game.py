class BlackjackGame:
    """Encapsulates the rules for a standard game of Blackjack."""

    @staticmethod
    def get_hand_value(hand):
        """Calculates the Blackjack value of a hand of cards."""
        value = 0
        num_aces = 0
        for card in hand:
            if card.rank in 'JQK':
                value += 10
            elif card.rank == 'A':
                num_aces += 1
                value += 11
            else:
                value += int(card.rank)

        # Demote aces from 11 to 1 if the total value is over 21
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

class JokerBlackjackGame(BlackjackGame):
    """Encapsulates the rules for a Blackjack variant with a Joker."""

    @staticmethod
    def get_hand_value(hand):
        """
        Overrides the base method to handle the Joker rule.
        Any hand with a Joker is automatically worth 21.
        """
        if any(card.rank == 'Joker' for card in hand):
            return 21
        # Fall back to the parent class's logic for hands without a Joker
        return super(JokerBlackjackGame, JokerBlackjackGame).get_hand_value(hand)
