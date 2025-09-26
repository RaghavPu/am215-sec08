from .deck import Deck
from .game import BlackjackGame, JokerBlackjackGame
from .visualize import plot_wealth_trajectories

# --- Game Parameters and Strategy ---

PLAYER_BLIND_THRESHOLD = 17
PLAYER_INFORMED_CONSERVATIVE_THRESHOLD = 12
DEALER_STRATEGY_THRESHOLD = 17
N_ROUNDS = 5000
N_TRAJECTORIES = 25
INITIAL_WEALTH = 100


def blind_player_strategy(player_hand, dealer_up_card, game_rules):
    """A simple strategy that ignores the dealer's up-card."""
    player_value = game_rules.get_hand_value(player_hand)
    return player_value < PLAYER_BLIND_THRESHOLD


def informed_player_strategy(player_hand, dealer_up_card, game_rules):
    """
    A more informed strategy that considers the dealer's up-card.
    Stands on a lower total if the dealer shows a weak card (2-6).
    """
    player_value = game_rules.get_hand_value(player_hand)
    dealer_up_card_rank = dealer_up_card.rank

    is_dealer_weak = dealer_up_card_rank in "23456"

    if is_dealer_weak:
        # Be more conservative if dealer is weak
        return player_value < PLAYER_INFORMED_CONSERVATIVE_THRESHOLD
    else:
        # Be more aggressive if dealer is strong
        return player_value < PLAYER_BLIND_THRESHOLD


def dealer_strategy(dealer_hand, game_rules):
    """Determines if the dealer should 'hit' or 'stand'."""
    dealer_value = game_rules.get_hand_value(dealer_hand)
    # Fixed strategy: dealer hits until 17 or more.
    return dealer_value < DEALER_STRATEGY_THRESHOLD


def play_round(deck, game_rules, player_strategy_fn):
    """Plays a single round of Blackjack and returns the outcome."""
    # --- Initial Deal ---
    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]
    dealer_up_card = dealer_hand[0]

    # --- Player's Turn ---
    while player_strategy_fn(player_hand, dealer_up_card, game_rules):
        player_hand.append(deck.draw())
        if game_rules.get_hand_value(player_hand) > 21:
            return -1  # Player busts

    # --- Dealer's Turn ---
    while dealer_strategy(dealer_hand, game_rules):
        dealer_hand.append(deck.draw())
        if game_rules.get_hand_value(dealer_hand) > 21:
            return 1  # Dealer busts

    # --- Determine Winner ---
    player_value = game_rules.get_hand_value(player_hand)
    dealer_value = game_rules.get_hand_value(dealer_hand)

    if player_value > dealer_value:
        return 1  # Player wins
    elif player_value < dealer_value:
        return -1  # Dealer wins
    else:
        return 0  # Push (tie)


def run_simulation(n_rounds, deck_factory, game_rules, player_strategy_fn):
    """Runs a full simulation and returns the player's wealth trajectory."""
    wealth = INITIAL_WEALTH
    wealth_history = [wealth]

    for _ in range(n_rounds):
        deck = deck_factory()
        deck.shuffle()
        outcome = play_round(deck, game_rules, player_strategy_fn)
        wealth += outcome
        wealth_history.append(wealth)
        if wealth <= 0:
            break

    return wealth_history


def main():
    """Runs and compares multiple Blackjack simulations with different strategies."""
    scenarios = {
        "Standard Game, Blind Strategy": (Deck, BlackjackGame, blind_player_strategy),
        "Joker Game, Blind Strategy": (
            Deck.create_deck_with_joker,
            JokerBlackjackGame,
            blind_player_strategy,
        ),
        "Standard Game, Informed Strategy": (
            Deck,
            BlackjackGame,
            informed_player_strategy,
        ),
        "Joker Game, Informed Strategy": (
            Deck.create_deck_with_joker,
            JokerBlackjackGame,
            informed_player_strategy,
        ),
    }

    results = {}
    for name, (deck_factory, game_rules, player_strategy_fn) in scenarios.items():
        print(f"Running simulation: {name}...")
        trajectories = []
        for i in range(N_TRAJECTORIES):
            history = run_simulation(
                N_ROUNDS, deck_factory, game_rules, player_strategy_fn
            )
            trajectories.append(history)
        results[name] = trajectories

    print("Generating plot...")
    plot_wealth_trajectories(results, "blackjack_comparison.png")
    print("Plot saved to blackjack_comparison.png")


if __name__ == "__main__":
    main()
