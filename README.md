# Extended Cluedo Game

This is an enhanced command-line version of the classic Cluedo (Clue) board game, featuring additional features and an expanded mansion.

## Requirements
- Python 3.6 or higher

## How to Run the Game
- Clone the repository 
- Navigate to the source code directory
- Run the game with Python:
   ```
   python main.py
   ```


## Game Features
- **Expanded Mansion**: 9 main rooms with connecting hallways
- **Hallway System**: Navigate through hallways connecting rooms
- **Multiple Characters**: 6 playable characters
- **Multiple Weapons**: 6 weapons scattered throughout the mansion
- **Secret Passages**: Hidden passages between specific rooms
- **Suggestions System**: Make suggestions when entering rooms
- **Card Distribution**: Automatic card dealing at game start
- **Turn-based Gameplay**: Dice rolls and movement points
- **Real-time Game State**: View current positions and available moves

## Game rules and play
1. Select the number of players (3-6)**
2. The game automatically distributes cards and establishes starting positions.
3. Players take turns rolling dice and traversing the mansion.
4. Upon entering a main room, players propose suggestions.
5. Suggestions facilitate the movement of characters and weapons to the current room.
6. Players employ deduction to unravel the mystery.
7. The game concludes when a player accurately accuses an individual.

## Available Commands
- `move [room name]` - Move to an adjacent room (uses 1 move)
- `suggest [character] [weapon]` - Make a suggestion (auto-triggered in rooms)
- `status` - Show your current status and position
- `map` - Show the mansion map with your current location
- `help` - Show game instructions
- `end` - End your turn
- `quit` - Exit the game

## Examples
- `move "Dining Room"` - Move to Dining Room (will auto-trigger suggestion if it's a main room)
- `suggest "Miss Scarlett" Revolver` - Suggest Miss Scarlett with the Revolver in your current room

## Characters (6)
- Miss Scarlett
- Colonel Mustard  
- Mrs. White
- Reverend Green
- Mrs. Peacock
- Professor Plum

## Weapons (6)
- Candlestick
- Dagger
- Lead Pipe
- Revolver
- Rope
- Wrench

## Rooms (9 Main Rooms)
- Kitchen
- Ballroom
- Conservatory
- Dining Room
- Billiard Room
- Library
- Lounge
- Hall
- Study

## Secret Passages
- Study ↔ Kitchen
- Conservatory ↔ Lounge

## Project Structure
- `main.py` - Entry point of the game, handles user input and game flow
- `game.py` - Main game logic, turn management, and player actions
- `mansion.py` - Mansion layout, navigation, and room management
- `layout.py` - Character, weapon, and room class definitions

## Game Flow
1. Choose number of players (3-6)
2. Game automatically distributes cards and sets up starting positions
3. Players take turns rolling dice and moving through the mansion
4. When entering a main room, players must make suggestions
5. Suggestions move characters and weapons to the current room
6. Players use deduction to solve the mystery
7. Game continues until a player makes the correct accusation

## Important Rules
- You can only make suggestions when in main rooms (not hallways)
- Every time you enter a room, you MUST make a suggestion
- Suggestions automatically move the accused character and weapon to your current room
- Movement uses hallways to connect between main rooms
- Secret passages allow instant movement between specific rooms

Enjoy solving the mystery in this enhanced Cluedo experience!