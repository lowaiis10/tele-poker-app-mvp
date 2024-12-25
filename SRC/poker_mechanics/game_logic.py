import random
from bot.database import add_player, create_game_entry, update_game_state, fetch_active_game

# Create a new poker game
def create_new_game(chat_id):
    """
    Creates a new game entry in the database.
    Args:
        chat_id (int): The chat ID of the group or private chat.
    Returns:
        int: The game ID of the newly created game.
    """
    try:
        game_id = create_game_entry(chat_id, "waiting")
        print(f"Game {game_id} created for chat {chat_id}.")
        return game_id
    except Exception as e:
        print(f"Error in create_new_game: {e}")
        return None

# Add a player to the game
def add_player_to_game(chat_id, user_id, username):
    """
    Adds a player to the game.
    Args:
        chat_id (int): The chat ID where the game is being played.
        user_id (int): Telegram user ID of the player.
        username (str): Telegram username of the player.
    Returns:
        bool: True if the player was added successfully, False otherwise.
    """
    try:
        game_id = fetch_active_game(chat_id)
        if not game_id:
            print(f"No active game found for chat_id {chat_id}.")
            return False

        add_player(game_id, user_id, username)
        print(f"Player {username} added to game {game_id}.")
        return True
    except Exception as e:
        print(f"Error in add_player_to_game: {e}")
        return False

# Start the poker game
def start_poker_game(chat_id):
    """
    Starts a poker game for the given chat.
    Args:
        chat_id (int): The chat ID of the group or private chat.
    Returns:
        bool: True if the game started successfully, False otherwise.
    """
    try:
        game_id = fetch_active_game(chat_id)
        if not game_id:
            print(f"No active game found for chat_id {chat_id}.")
            return False

        update_game_state(game_id, "in_progress")
        print(f"Game {game_id} started for chat_id {chat_id}.")
        return True
    except Exception as e:
        print(f"Error in start_poker_game: {e}")
        return False

# Deal cards to players
def deal_cards(players):
    """
    Deals two cards to each player.
    Args:
        players (list): List of player usernames or IDs.
    Returns:
        dict: A dictionary mapping player IDs/usernames to their hands.
    """
    try:
        deck = generate_deck()
        random.shuffle(deck)
        player_hands = {}

        for player in players:
            hand = [deck.pop(), deck.pop()]
            player_hands[player] = hand

        print(f"Dealt cards: {player_hands}")
        return player_hands
    except Exception as e:
        print(f"Error in deal_cards: {e}")
        return {}

# Generate a standard 52-card deck
def generate_deck():
    """
    Generates a standard 52-card deck.
    Returns:
        list: A list of card strings in the format "RankSuit" (e.g., "AS" for Ace of Spades).
    """
    suits = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [f"{rank}{suit}" for suit in suits for rank in ranks]

# Simulate a round of poker (e.g., flop, turn, river)
def simulate_round(player_hands):
    """
    Simulates a full poker round, including the flop, turn, and river.
    Args:
        player_hands (dict): Dictionary of player hands.
    Returns:
        dict: A summary of the round, including the community cards and player hands.
    """
    try:
        deck = generate_deck()
        random.shuffle(deck)

        # Burn one card before dealing community cards (as per poker rules)
        deck.pop()

        # The Flop (3 cards)
        flop = [deck.pop() for _ in range(3)]

        # Burn one card
        deck.pop()

        # The Turn (1 card)
        turn = deck.pop()

        # Burn one card
        deck.pop()

        # The River (1 card)
        river = deck.pop()

        community_cards = flop + [turn, river]
        print(f"Community Cards: {community_cards}")
        return {
            "player_hands": player_hands,
            "community_cards": community_cards,
        }
    except Exception as e:
        print(f"Error in simulate_round: {e}")
        return {}

# Example logic to determine a winner (placeholder)
def determine_winner(player_hands, community_cards):
    """
    Determines the winner of the poker round (simplified logic).
    Args:
        player_hands (dict): Dictionary of player hands.
        community_cards (list): List of community cards.
    Returns:
        str: The winner's ID or username.
    """
    try:
        # Placeholder logic: Randomly select a winner
        winner = random.choice(list(player_hands.keys()))
        print(f"The winner is: {winner}")
        return winner
    except Exception as e:
        print(f"Error in determine_winner: {e}")
        return None
