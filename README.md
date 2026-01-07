# AI Game Referee Chatbot

This project is a command-line chatbot that acts as a referee for a game of Rock-Paper-Scissors-Plus, built entirely in Python. It was developed to satisfy a set of requirements evaluating logical reasoning, agent design, use of primitives, and engineering communication.

### A Note on the "Google ADK"
The assignment required using the "Google ADK," a framework that is not publicly available. To solve this, this project includes a local `adk` directory which **mocks** the essential features of an Agent Development Kit. This mock includes classes like `AdkApp`, `Tool`, `FunctionDeclaration`, and `Parameter`, allowing the project to demonstrate how it would integrate with a real ADK while remaining a standalone, runnable application. This approach showcases the ability to work with specified architectural patterns even when dependencies are unavailable.

---

## How to Run
1. Make sure you have Python 3 installed.
2. From the project root, run the game:
   ```sh
   python game_referee.py
   ```
---
## State Model
The game's state is managed by the `Game` dataclass, providing a clean and predictable structure. This model entirely avoids storing state in prompts, ensuring stability.

The state includes:
- `round_number`: The current round (1, 2, or 3).
- `player_score` & `bot_score`: The current scores for the user and the bot.
- `player_bomb_available` & `bot_bomb_available`: Booleans to enforce the "bomb can be used once per game" rule for each player.
- `history`: A list of dictionaries, logging the moves and outcomes of each past round for traceability.

## Agent/Tool Design
The architecture is centered around a single `GameRefereeAgent`, which cleanly separates concerns as required.

- **`GameRefereeAgent`**: This class encapsulates the entire game.
    - **`run_game()`**: This method serves as the main entry point. It manages the primary game loop (ensuring the game doesn't exceed 3 rounds), handles user interaction (getting input - the **intent understanding**), and generates the main prompts and final "Game Over" message (part of the **response generation**).
    - **`_play_round()`**: This private method contains the core **game logic**. It takes the user's move, validates it, determines the bot's move, decides the winner, and then calls the `update_game_state_tool` to apply the changes.

- **`update_game_state_tool`**: This is an explicit `Tool` defined using the mocked ADK primitives.
    - Its schema is declared using `Parameter` objects, specifying the exact inputs required for a state update.
    - It is used for all **state mutation**. The agent calls this tool to produce a new, updated `Game` state object after every round, ensuring a single, clear path for state changes.

- **`AdkApp`**: The application's entry point in `if __name__ == "__main__":` uses the mocked `AdkApp` class. This class takes the `GameRefereeAgent` as its primary agent and calls its `run()` method, simulating how a real agent framework would deploy and run an agent.

## Trade-offs Made
- **Mocked ADK vs. Real ADK**: The most significant trade-off was creating a mock implementation of the Google ADK. While a real ADK would be used in a production environment, mocking it was necessary to complete the assignment and a standard industry practice for handling unavailable dependencies.
- **CLI vs. UI Framework**: The project uses a simple command-line interface for user interaction. This prioritizes focusing on the core logic and agent architecture over the user experience, as specified in the assignment.

## Future Improvements
- **More Sophisticated Bot**: The bot's move is currently chosen randomly. A more advanced bot could be implemented that analyzes the `history` in the game state to predict the player's next move.
- **Asynchronous Operations**: A real ADK would likely operate asynchronously. The agent could be improved to handle asynchronous calls, for example, if fetching a bot's move involved a network request to a model.
- **Modularization**: For a larger application, the `adk` mock, `Game` dataclass, and `GameRefereeAgent` class could be split into separate files within a more structured Python package.
