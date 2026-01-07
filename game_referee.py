
import random
from dataclasses import dataclass, field
from adk.api import AdkApp, Tool
from adk.schema import String, List, Dict, related_type_name, Parameter

# Game Rules
RULES = """
Welcome to Rock-Paper-Scissors-Plus!
- Best of 3 rounds.
- Moves: rock, paper, scissors, or bomb (once per game).
- Bomb beats all, but bomb vs bomb is a draw.
- Invalid moves waste a round. Let's begin!
- Game Ends after 3 rounds; highest score wins.
"""

VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

@dataclass
class Game:
    """A class to represent the game state."""
    round_number: int = 1
    player_score: int = 0
    bot_score: int = 0
    player_bomb_available: bool = True
    bot_bomb_available: bool = True
    history: list = field(default_factory=list)

    def to_dict(self):
        return {
            "round_number": self.round_number,
            "player_score": self.player_score,
            "bot_score": self.bot_score,
            "player_bomb_available": self.player_bomb_available,
            "bot_bomb_available": self.bot_bomb_available,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

def update_game_state(
    round_number: int,
    player_score: int,
    bot_score: int,
    player_bomb_available: bool,
    bot_bomb_available: bool,
    history: list,
) -> Game:
    """Updates the game state."""
    game = Game(
        round_number=round_number,
        player_score=player_score,
        bot_score=bot_score,
        player_bomb_available=player_bomb_available,
        bot_bomb_available=bot_bomb_available,
        history=history,
    )
    return game

update_game_state_tool = Tool(
    name="update_game_state",
    description="Updates the game state.",
    func=update_game_state,
    output_type=Game,
    parameters=[
        Parameter(name="round_number", type=int, description="The current round number"),
        Parameter(name="player_score", type=int, description="The player's score"),
        Parameter(name="bot_score", type=int, description="The bot's score"),
        Parameter(name="player_bomb_available", type=bool, description="Whether the player's bomb is available"),
        Parameter(name="bot_bomb_available", type=bool, description="Whether the bot's bomb is available"),
        Parameter(name="history", type=list, description="A list of past rounds' data"),
    ]
)

class GameRefereeAgent:
    """An agent that referees a game of Rock-Paper-Scissors-Plus."""

    def __init__(self):
        self.game = Game()
        self.update_tool = update_game_state_tool

    def _play_round(self, player_move: str) -> None:
        """Plays a single round of the game and updates the game state."""
        # Validate player's move
        if player_move not in VALID_MOVES:
            print("Invalid move! This round is wasted.")
            winner = "bot"
            bot_move = None
        elif player_move == "bomb" and not self.game.player_bomb_available:
            print("You have already used your bomb! This round is wasted.")
            winner = "bot"
            bot_move = None
        else:
            # Bot's move
            bot_moves = VALID_MOVES.copy()
            if not self.game.bot_bomb_available:
                bot_moves.remove("bomb")
            bot_move = random.choice(bot_moves)

            print(f"You chose: {player_move}")
            print(f"The bot chose: {bot_move}")

            # Determine the winner
            if player_move == bot_move:
                winner = "draw"
            elif player_move == "bomb":
                winner = "player"
            elif bot_move == "bomb":
                winner = "bot"
            elif (player_move == "rock" and bot_move == "scissors") or \
                    (player_move == "scissors" and bot_move == "paper") or \
                    (player_move == "paper" and bot_move == "rock"):
                winner = "player"
            else:
                winner = "bot"

        # Update scores and game state
        if winner == "player":
            self.game.player_score += 1
            print("You win this round!")
        elif winner == "bot":
            self.game.bot_score += 1
            print("The bot wins this round!")
        else:
            print("This round is a draw!")

        if player_move == "bomb":
            self.game.player_bomb_available = False
        if bot_move == "bomb":
            self.game.bot_bomb_available = False

        history_entry = {"player_move": player_move, "bot_move": bot_move, "winner": winner}
        
        # Use the tool to update the game state
        self.game = self.update_tool.func(
            round_number=self.game.round_number + 1,
            player_score=self.game.player_score,
            bot_score=self.game.bot_score,
            player_bomb_available=self.game.player_bomb_available,
            bot_bomb_available=self.game.bot_bomb_available,
            history=self.game.history + [history_entry],
        )

    def run_game(self):
        """Starts and runs the entire game."""
        print(RULES)
        
        while self.game.round_number <= 3:
            print(f"\n--- Round {self.game.round_number} ---")
            player_move = input("Enter your move (rock, paper, scissors, or bomb): ").lower()
            self._play_round(player_move)

        print("\n--- Game Over ---")
        if self.game.player_score > self.game.bot_score:
            print("You are the winner!")
        elif self.game.bot_score > self.game.player_score:
            print("The bot is the winner!")
        else:
            print("The game is a draw!")

        print(f"Final Score: You {self.game.player_score} - {self.game.bot_score} Bot")
        print("Game state:")
        print(self.game)


if __name__ == "__main__":
    app = AdkApp(agent=GameRefereeAgent(), description="Rock-Paper-Scissors-Plus Game Referee")
    app.run()
