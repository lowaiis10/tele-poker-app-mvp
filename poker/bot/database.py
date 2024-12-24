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
            joined_at TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    """)

    # Table to store game logs (optional for debugging or analytics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            log_message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    """)

    connection.commit()
    connection.close()
    print("✅ Tables created successfully.")


def create_game_entry(chat_id, state):
    """
    Create a new game entry in the database.
    Parameters:
    - chat_id (int): The Telegram chat ID.
    - state (str): The initial state of the game.
    Returns:
    - int: The ID of the newly created game.
    """
    connection = connect()
    cursor = connection.cursor()

    created_at = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO games (chat_id, state, created_at)
        VALUES (?, ?, ?)
    """, (chat_id, state, created_at))

    game_id = cursor.lastrowid  # Get the ID of the newly created game
    connection.commit()
    connection.close()

    return game_id


def add_player(game_id, user_id, username):
    """
    Add a player to the game.
    Parameters:
    - game_id (int): The ID of the game.
    - user_id (int): The Telegram user ID of the player.
    - username (str): The Telegram username of the player.
    """
    connection = connect()
    cursor = connection.cursor()

    joined_at = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO players (game_id, user_id, username, joined_at)
        VALUES (?, ?, ?, ?)
    """, (game_id, user_id, username, joined_at))

    connection.commit()
    connection.close()


def fetch_active_game(chat_id):
    """
    Fetch the active game for a given chat ID.
    Parameters:
    - chat_id (int): The Telegram chat ID.
    Returns:
    - int: The ID of the active game, or None if no active game exists.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM games
        WHERE chat_id = ? AND (state = 'waiting' OR state = 'in_progress')
        ORDER BY created_at DESC
        LIMIT 1
    """, (chat_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None


def update_game_state(game_id, new_state):
    """
    Update the state of a game in the database.
    Parameters:
    - game_id (int): The ID of the game.
    - new_state (str): The new state to set for the game.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE games
        SET state = ?
        WHERE id = ?
    """, (new_state, game_id))
    connection.commit()
    connection.close()


def fetch_players_in_game(game_id):
    """
    Fetch all players in a given game.
    Parameters:
    - game_id (int): The ID of the game.
    Returns:
    - list: A list of tuples containing user_id and username.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT user_id, username FROM players WHERE game_id = ?
    """, (game_id,))
    players = cursor.fetchall()
    connection.close()
    return players


def log_game_event(game_id, message):
    """
    Log an event for a game.
    Parameters:
    - game_id (int): The ID of the game.
    - message (str): The log message.
    """
    connection = connect()
    cursor = connection.cursor()

    created_at = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO logs (game_id, log_message, created_at)
        VALUES (?, ?, ?)
    """, (game_id, message, created_at))

    connection.commit()
    connection.close()


def fetch_game_logs(game_id):
    """
    Fetch logs for a given game.
    Parameters:
    - game_id (int): The ID of the game.
    Returns:
    - list: A list of log messages.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT log_message FROM logs WHERE game_id = ?
        ORDER BY created_at ASC
    """, (game_id,))
    logs = [log[0] for log in cursor.fetchall()]
    connection.close()
    return logs


# Initialize the database
if __name__ == "__main__":
    create_tables()
