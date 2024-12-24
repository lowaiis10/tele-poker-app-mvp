def format_players(players):
    """Format player list for output."""
    return "\n".join([f"@{player[1]}" for player in players])

def calculate_pot(bets):
    """Calculate the total pot from bets."""
    return sum(bets.values())
