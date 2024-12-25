import sqlite3
from datetime import datetime

DB_FILE = "poker_bot.db"  # Name of the database file


def connect():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def create_tables():
    """Create the necessary tables for the poker bot."""
    connection = connect()
    cursor = connection.cursor()

    # Table to store game information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            state TEXT NOT NULL,  -- Game state: "waiting", "in_progress", "completed"
            small_blind REAL NOT NULL,
            big_blind REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Table to store player information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            cash_in REAL NOT NULL,  -- Amount of SOL the player buys in with
            joined_at TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    """)

    connection.commit()
    connection.close()
    print("✅ Tables created successfully.")


def create_game_entry(chat_id, small_blind, big_blind):
    """Create a new game entry in the database."""
    connection = connect()
    cursor = connection.cursor()

    created_at = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO games (chat_id, state, small_blind, big_blind, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (chat_id, "waiting", small_blind, big_blind, created_at))

    game_id = cursor.lastrowid  # Get the ID of the newly created game
    connection.commit()
    connection.close()

    return game_id


def add_player(game_id, user_id, username, cash_in):
    """Add a player to the game."""
    connection = connect()
    cursor = connection.cursor()

    joined_at = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO players (game_id, user_id, username, cash_in, joined_at)
        VALUES (?, ?, ?, ?, ?)
    """, (game_id, user_id, username, cash_in, joined_at))

    connection.commit()
    connection.close()


def fetch_active_game(chat_id, small_blind, big_blind):
    """Fetch an active game matching the chat and blind values."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM games
        WHERE chat_id = ? AND state = ? AND small_blind = ? AND big_blind = ?
    """, (chat_id, "waiting", small_blind, big_blind))

    game = cursor.fetchone()
    connection.close()

    return game


def update_game_state(game_id, new_state):
    """Update the state of a game in the database."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE games SET state = ? WHERE id = ?",
        (new_state, game_id)
    )

    connection.commit()
    connection.close()
