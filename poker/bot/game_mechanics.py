import random

# Deck management
def create_deck():
    """Create a standard 52-card deck."""
    suits = ["♠️", "♥️", "♦️", "♣️"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [rank + suit for suit in suits for rank in ranks]

def shuffle_deck(deck):
    """Shuffle the deck."""
    random.shuffle(deck)
    return deck

def deal_cards(deck, num_cards):
    """Deal a specified number of cards from the deck."""
    cards = deck[:num_cards]
    del deck[:num_cards]
    return cards

# Game setup
def start_new_game(players):
    """
    Initializes a new poker game.
    players: List of player dictionaries with `id` and `username`.
    """
    game_state = {
        "deck": shuffle_deck(create_deck()),
        "pot": 0,
        "players": {
            player["id"]: {
                "hand": [],
                "balance": 1000,  # Default balance for each player
                "active": True,   # Whether the player is still in the game
                "bet": 0          # Current bet amount
            } 
            for player in players
        },
        "community_cards": [],
        "current_bet": 0,  # The highest bet in the current round
        "turn": 0,         # Keeps track of whose turn it is
        "state": "pre-flop"  # Game state: pre-flop, flop, turn, river
    }
    return game_state

# Betting logic
def place_bet(player_id, amount, game_state):
    """
    Handles a player's bet.
    """
    player = game_state["players"][player_id]
    if player["balance"] >= amount:
        player["balance"] -= amount
        player["bet"] += amount
        game_state["pot"] += amount
        game_state["current_bet"] = max(game_state["current_bet"], amount)
        return f"Player {player_id} bet {amount}. Current pot: {game_state['pot']}"
    else:
        return "Insufficient balance!"

def fold(player_id, game_state):
    """
    Handles a player folding.
    """
    game_state["players"][player_id]["active"] = False
    return f"Player {player_id} has folded."

# Deal community cards
def deal_community_cards(deck, game_state, num_cards):
    """
    Deals community cards (flop, turn, river).
    """
    new_cards = deal_cards(deck, num_cards)
    game_state["community_cards"].extend(new_cards)
    return f"Community cards: {game_state['community_cards']}"

# Hand evaluation
def evaluate_hand(player_hand, community_cards):
    """
    Simplified hand evaluation for now.
    Combine player hand and community cards and return them sorted by rank.
    """
    ranks = "23456789TJQKA"
    all_cards = player_hand + community_cards
    sorted_hand = sorted(all_cards, key=lambda card: ranks.index(card[:-1]), reverse=True)
    return sorted_hand

# Advance turn
def advance_turn(game_state):
    """
    Moves the game to the next player's turn.
    """
    player_ids = list(game_state["players"].keys())
    while True:
        game_state["turn"] = (game_state["turn"] + 1) % len(player_ids)
        current_player = player_ids[game_state["turn"]]
        if game_state["players"][current_player]["active"]:
            return f"It is now Player {current_player}'s turn."

# Check winner
def determine_winner(game_state):
    """
    Determines the winner based on a simple hand evaluation.
    """
    best_hand = None
    best_player = None
    for player_id, player in game_state["players"].items():
        if player["active"]:
            hand = evaluate_hand(player["hand"], game_state["community_cards"])
            if best_hand is None or hand > best_hand:
                best_hand = hand
                best_player = player_id
    return f"Player {best_player} wins with hand {best_hand}!"

# Main game flow
def poker_round(game_state):
    """
    Simulates one round of poker (simplified).
    """
    # Deal cards to players
    for player_id, player in game_state["players"].items():
        player["hand"] = deal_cards(game_state["deck"], 2)
    print("Cards dealt to players.")

    # Flop
    print(deal_community_cards(game_state["deck"], game_state, 3))

    # Turn
    print(deal_community_cards(game_state["deck"], game_state, 1))

    # River
    print(deal_community_cards(g))
